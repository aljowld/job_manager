"""Real job source connector for the public Arbeitnow Job Board API."""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

import httpx

from app.collection.base import RawJob

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://www.arbeitnow.com/api/job-board-api"
DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_PAGES = 2
USER_AGENT = "job-manager/0.1 (personal job search assistant; +https://github.com/)"


class ArbeitnowApiError(Exception):
    """Raised when the Arbeitnow API response cannot be turned into raw jobs."""


class ArbeitnowJobSource:
    """Fetches public postings from the Arbeitnow Job Board API (no API key required)."""

    source_name = "arbeitnow"
    source_url = "https://www.arbeitnow.com"
    collection_method = "api"

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_pages: int = DEFAULT_MAX_PAGES,
        client: httpx.Client | None = None,
    ) -> None:
        self._base_url = base_url
        self._timeout = timeout
        self._max_pages = max_pages
        self._client = client

    def collect(self) -> list[RawJob]:
        """Collect raw jobs across pages, stopping at max_pages or an empty page."""
        client = self._client or httpx.Client(
            timeout=self._timeout, headers={"User-Agent": USER_AGENT}
        )
        owns_client = self._client is None
        raw_jobs: list[RawJob] = []
        try:
            for page in range(1, self._max_pages + 1):
                items = self._fetch_page(client, page)
                if not items:
                    break
                for item in items:
                    raw_job = self._parse_item(item)
                    if raw_job is not None:
                        raw_jobs.append(raw_job)
        finally:
            if owns_client:
                client.close()
        return raw_jobs

    def _fetch_page(self, client: httpx.Client, page: int) -> list[dict[str, Any]]:
        try:
            response = client.get(self._base_url, params={"page": page})
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise ArbeitnowApiError(f"Arbeitnow API timed out on page {page}") from exc
        except httpx.HTTPStatusError as exc:
            raise ArbeitnowApiError(
                f"Arbeitnow API returned status {exc.response.status_code} on page {page}"
            ) from exc
        except httpx.HTTPError as exc:
            raise ArbeitnowApiError(f"Arbeitnow API request failed on page {page}: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise ArbeitnowApiError(f"Arbeitnow API returned invalid JSON on page {page}") from exc

        data = payload.get("data") if isinstance(payload, dict) else None
        if not isinstance(data, list):
            raise ArbeitnowApiError(f"Arbeitnow API response missing a 'data' list on page {page}")
        return data

    def _parse_item(self, item: dict[str, Any]) -> RawJob | None:
        slug = item.get("slug")
        title = item.get("title")
        url = item.get("url")
        if not slug or not title or not url:
            logger.warning(
                "Skipping Arbeitnow item with missing slug, title or url: %r", item.get("slug")
            )
            return None

        job_types = [str(value) for value in (item.get("job_types") or [])]
        tags = [str(value) for value in (item.get("tags") or [])]

        return RawJob(
            source_name=self.source_name,
            external_job_id=str(slug),
            source_url=str(url),
            title=str(title),
            company_name=self._clean_str(item.get("company_name")),
            description=self._clean_str(item.get("description")),
            location_raw=self._clean_str(item.get("location")),
            contract_type_raw="; ".join(job_types) if job_types else None,
            remote_type_raw="remote" if item.get("remote") is True else None,
            salary_raw=None,
            publication_date_raw=self._format_created_at(item.get("created_at")),
            experience_level_raw=None,
            technologies=tags,
            metadata={"job_types": job_types},
        )

    @staticmethod
    def _clean_str(value: Any) -> str | None:
        if value is None:
            return None
        text = str(value).strip()
        return text or None

    @staticmethod
    def _format_created_at(value: Any) -> str | None:
        if value is None:
            return None
        try:
            timestamp = int(value)
        except (TypeError, ValueError):
            return None
        return datetime.fromtimestamp(timestamp, tz=UTC).isoformat()
