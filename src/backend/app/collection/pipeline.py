from __future__ import annotations

import hashlib
import json
import logging
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import exc, select
from sqlalchemy.orm import Session

from app.collection.base import JobCollector, RawJob
from app.db.models import JobOffer, JobSource, JobSourceOccurrence, RawJobSnapshot
from app.deduplication.jobs import DuplicateDecision, JobDeduplicator

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class PipelineResult:
    collected: int
    persisted: int
    failed: int


class CollectionPipeline:
    """Minimal pipeline linking a source to the existing persistence models."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.deduplicator = JobDeduplicator(db)

    def run(self, source: JobCollector) -> PipelineResult:
        """Collect, snapshot, normalize and persist raw jobs for a single source."""
        collected_jobs = source.collect()
        result = PipelineResult(collected=len(collected_jobs), persisted=0, failed=0)

        persisted_source = self._ensure_source(source)
        for raw_job in collected_jobs:
            try:
                with self.db.begin_nested():
                    self._persist_one(persisted_source, raw_job)
            except (ValueError, exc.SQLAlchemyError) as exc_info:
                logger.warning(
                    "Skipping raw job %s from source %s: %s",
                    getattr(raw_job, "external_job_id", None),
                    getattr(source, "source_name", None),
                    exc_info,
                )
                result.failed += 1
                continue

            result.persisted += 1

        self.db.commit()
        return result

    def _ensure_source(self, source: JobCollector) -> JobSource:
        existing = self.db.scalar(select(JobSource).where(JobSource.name == source.source_name))
        if existing is not None:
            return existing

        job_source = JobSource(
            name=source.source_name,
            base_url=getattr(source, "source_url", None),
            collection_method=getattr(source, "collection_method", None) or "generic",
            enabled=True,
            metadata_={"source_name": source.source_name},
        )
        self.db.add(job_source)
        self.db.flush()
        return job_source

    def _persist_one(self, source: JobSource, raw_job: RawJob) -> None:
        self._validate_raw_job(raw_job)

        normalized_title = self._normalize_title(raw_job.title)
        normalized_company = self._normalize_company(raw_job.company_name)
        normalized_city = self._normalize_city(raw_job.location_raw)
        normalized_contract = self._normalize_contract(raw_job.contract_type_raw)
        content_hash = self._content_hash(raw_job)

        snapshot = RawJobSnapshot(
            source_id=source.id,
            external_job_id=raw_job.external_job_id,
            source_url=raw_job.source_url,
            payload=self._payload_for_snapshot(raw_job),
            raw_html=None,
            content_hash=content_hash,
            collected_at=datetime.now(UTC),
        )
        self.db.add(snapshot)
        self.db.flush()

        duplicate_decision = self.deduplicator.decide(
            title=normalized_title,
            company_name=normalized_company,
            city=normalized_city,
            contract_type=normalized_contract,
            source_id=source.id,
            external_job_id=raw_job.external_job_id,
            source_url=raw_job.source_url,
            content_hash=content_hash,
        )

        if duplicate_decision.decision == DuplicateDecision.CONFIRMED_DUPLICATE:
            existing_offer = duplicate_decision.job_offer
            if existing_offer is None:
                raise ValueError("Confirmed duplicate requires an existing canonical offer")

            occurrence = self.db.scalar(
                select(JobSourceOccurrence).where(
                    JobSourceOccurrence.job_offer_id == existing_offer.id,
                    JobSourceOccurrence.source_id == source.id,
                    JobSourceOccurrence.external_job_id == raw_job.external_job_id,
                )
            )
            if occurrence is None:
                occurrence = JobSourceOccurrence(
                    job_offer_id=existing_offer.id,
                    source_id=source.id,
                    external_job_id=raw_job.external_job_id,
                    source_url=raw_job.source_url,
                    collected_at=datetime.now(UTC),
                    is_primary=True,
                    status="active",
                    created_at=datetime.now(UTC),
                )
                self.db.add(occurrence)
                self.db.flush()
            return

        job_offer = JobOffer(
            title=normalized_title,
            company_name=normalized_company,
            description=raw_job.description,
            normalized_description=raw_job.description,
            contract_type=normalized_contract,
            job_type=self._normalize_job_type(raw_job.metadata.get("job_type")),
            location_text=raw_job.location_raw,
            city=normalized_city,
            country=self._normalize_country(raw_job.metadata.get("country")),
            remote_type=self._normalize_remote(raw_job.remote_type_raw),
            salary_min=self._normalize_salary_min(raw_job.salary_raw),
            salary_max=self._normalize_salary_max(raw_job.salary_raw),
            publication_date=self._normalize_publication_date(raw_job.publication_date_raw),
            experience_level=self._normalize_experience(raw_job.experience_level_raw),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            status="active",
        )
        self.db.add(job_offer)
        self.db.flush()

        occurrence = JobSourceOccurrence(
            job_offer_id=job_offer.id,
            source_id=source.id,
            external_job_id=raw_job.external_job_id,
            source_url=raw_job.source_url,
            collected_at=datetime.now(UTC),
            is_primary=True,
            status="active",
            created_at=datetime.now(UTC),
        )
        self.db.add(occurrence)
        self.db.flush()

    def _validate_raw_job(self, raw_job: RawJob) -> None:
        if not raw_job.external_job_id or not raw_job.external_job_id.strip():
            raise ValueError("RawJob.external_job_id is required")
        if not raw_job.source_url or not raw_job.source_url.strip():
            raise ValueError("RawJob.source_url is required")
        if not raw_job.title or not raw_job.title.strip():
            raise ValueError("RawJob.title is required")

    def _payload_for_snapshot(self, raw_job: RawJob) -> dict[str, Any]:
        return {
            "source_name": raw_job.source_name,
            "external_job_id": raw_job.external_job_id,
            "source_url": raw_job.source_url,
            "title": raw_job.title,
            "company_name": raw_job.company_name,
            "description": raw_job.description,
            "location_raw": raw_job.location_raw,
            "contract_type_raw": raw_job.contract_type_raw,
            "remote_type_raw": raw_job.remote_type_raw,
            "salary_raw": raw_job.salary_raw,
            "publication_date_raw": raw_job.publication_date_raw,
            "experience_level_raw": raw_job.experience_level_raw,
            "technologies": raw_job.technologies,
            "metadata": raw_job.metadata,
        }

    def _content_hash(self, raw_job: RawJob) -> str:
        payload = self._payload_for_snapshot(raw_job)
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _normalize_title(self, title: str) -> str:
        cleaned = title.strip()
        if not cleaned:
            raise ValueError("Title is required")
        return cleaned

    def _normalize_company(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def _normalize_contract(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip().lower()
        mapping = {
            "cdi": "CDI",
            "cdd": "CDD",
            "internship": "internship",
            "full_time": "full_time",
            "contract": "contract",
            "freelance": "freelance",
        }
        return mapping.get(cleaned, value.strip())

    def _normalize_job_type(self, value: Any) -> str | None:
        if value is None:
            return None
        return str(value)

    def _normalize_city(self, location: str | None) -> str | None:
        if location is None:
            return None
        cleaned = location.strip()
        if not cleaned or cleaned.lower() == "remote":
            return None
        if "," in cleaned:
            return cleaned.split(",", 1)[0].strip()
        return cleaned

    def _normalize_country(self, value: Any) -> str | None:
        if value is None:
            return None
        country = str(value).strip()
        return country or None

    def _normalize_remote(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip().lower()
        if cleaned in {"remote", "hybrid", "on_site"}:
            return cleaned
        return cleaned

    @staticmethod
    def _parse_salary_part(raw_value: str) -> int | None:
        cleaned = raw_value.strip().lower()
        cleaned = cleaned.replace("€", "").replace("£", "").replace("$", "")
        cleaned = cleaned.replace("/an", "").replace("/yr", "").replace("year", "")
        cleaned = cleaned.replace(" ", "")
        if not cleaned:
            return None

        match = re.fullmatch(r"(?P<value>\d+)(?P<suffix>k|m)?", cleaned)
        if match is None:
            return None

        value = int(match.group("value"))
        suffix = match.group("suffix")
        if suffix == "k":
            return value * 1000
        if suffix == "m":
            return value * 1_000_000
        return value

    def _parse_salary_range(self, salary: str | None) -> tuple[int | None, int | None] | None:
        if salary is None:
            return None

        text = salary.strip().replace("€", "").replace("£", "").replace("$", "")
        if not text:
            return None

        candidates = re.split(r"-", text)
        if len(candidates) == 1:
            candidates = re.split(r"to", text, flags=re.IGNORECASE)
        if len(candidates) == 1:
            parsed = self._parse_salary_part(text)
            if parsed is None:
                return None
            return parsed, parsed

        minimum = self._parse_salary_part(candidates[0])
        maximum = self._parse_salary_part(candidates[1])
        if minimum is None or maximum is None:
            return None
        return minimum, maximum

    def _normalize_salary_min(self, salary: str | None) -> int | None:
        range_values = self._parse_salary_range(salary)
        if range_values is None:
            return None
        return range_values[0]

    def _normalize_salary_max(self, salary: str | None) -> int | None:
        range_values = self._parse_salary_range(salary)
        if range_values is None:
            return None
        return range_values[1]

    def _normalize_publication_date(self, value: str | None) -> datetime | None:
        if value is None:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)

    def _normalize_experience(self, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None
