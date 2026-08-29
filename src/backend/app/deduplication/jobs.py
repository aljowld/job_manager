from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlsplit, urlunsplit

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import JobOffer, JobSourceOccurrence, RawJobSnapshot


class DuplicateDecision(str, Enum):
    NOT_DUPLICATE = "NOT_DUPLICATE"
    POSSIBLE_DUPLICATE = "POSSIBLE_DUPLICATE"
    CONFIRMED_DUPLICATE = "CONFIRMED_DUPLICATE"


@dataclass(slots=True)
class DeduplicationResult:
    decision: DuplicateDecision
    job_offer: JobOffer | None = None
    reason: str | None = None


class JobDeduplicator:
    """Conservative, deterministic deduplication for job offers."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def decide(
        self,
        *,
        title: str | None,
        company_name: str | None,
        city: str | None,
        contract_type: str | None,
        source_id: int | None,
        external_job_id: str | None,
        source_url: str | None,
        content_hash: str | None = None,
    ) -> DeduplicationResult:
        if source_id is not None and external_job_id and external_job_id.strip():
            existing_occurrence = self.db.scalar(
                select(JobSourceOccurrence).where(
                    JobSourceOccurrence.source_id == source_id,
                    JobSourceOccurrence.external_job_id == external_job_id,
                )
            )
            if existing_occurrence is not None:
                return DeduplicationResult(
                    decision=DuplicateDecision.CONFIRMED_DUPLICATE,
                    job_offer=existing_occurrence.job_offer,
                    reason="same source + external_job_id",
                )

        normalized_url = self._normalize_url(source_url)
        if normalized_url:
            existing_occurrences = self.db.scalars(select(JobSourceOccurrence)).all()
            for existing_occurrence in existing_occurrences:
                if self._normalize_url(existing_occurrence.source_url) == normalized_url:
                    return DeduplicationResult(
                        decision=DuplicateDecision.CONFIRMED_DUPLICATE,
                        job_offer=existing_occurrence.job_offer,
                        reason="same normalized source_url",
                    )

        if content_hash:
            existing_snapshot = self.db.scalar(
                select(RawJobSnapshot).where(RawJobSnapshot.content_hash == content_hash)
            )
            if existing_snapshot is not None:
                existing_occurrence = self.db.scalar(
                    select(JobSourceOccurrence).where(
                        JobSourceOccurrence.source_id == existing_snapshot.source_id,
                        JobSourceOccurrence.external_job_id == existing_snapshot.external_job_id,
                    )
                )
                if existing_occurrence is not None:
                    return DeduplicationResult(
                        decision=DuplicateDecision.CONFIRMED_DUPLICATE,
                        job_offer=existing_occurrence.job_offer,
                        reason="same content_hash with prior snapshot",
                    )

        fingerprint = self._job_fingerprint(
            title=title,
            company_name=company_name,
            city=city,
            contract_type=contract_type,
        )
        if fingerprint:
            existing_offer = self.db.scalar(
                select(JobOffer).where(
                    JobOffer.title == title,
                    JobOffer.company_name == company_name,
                    JobOffer.city == city,
                    JobOffer.contract_type == contract_type,
                )
            )
            if existing_offer is not None:
                return DeduplicationResult(
                    decision=DuplicateDecision.POSSIBLE_DUPLICATE,
                    job_offer=existing_offer,
                    reason="matching deterministic fingerprint",
                )

        return DeduplicationResult(
            decision=DuplicateDecision.NOT_DUPLICATE,
            job_offer=None,
            reason="no strong duplicate signal",
        )

    @staticmethod
    def _normalize_url(url: str | None) -> str | None:
        if url is None:
            return None
        parsed = urlsplit(url)
        if not parsed.scheme or not parsed.netloc:
            return None
        normalized = parsed._replace(fragment="")
        return urlunsplit(normalized)

    @staticmethod
    def _job_fingerprint(
        *,
        title: str | None,
        company_name: str | None,
        city: str | None,
        contract_type: str | None,
    ) -> str | None:
        normalized_parts = [
            (title or "").strip(),
            (company_name or "").strip(),
            (city or "").strip(),
            (contract_type or "").strip(),
        ]
        if not any(part for part in normalized_parts):
            return None
        cleaned = [" ".join(part.split()).lower() for part in normalized_parts]
        return " | ".join(cleaned)
