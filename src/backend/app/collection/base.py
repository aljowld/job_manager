from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True, slots=True)
class RawJob:
    """Minimal typed representation of a job as it was received from a source."""

    source_name: str
    external_job_id: str
    source_url: str
    title: str
    company_name: str | None = None
    description: str | None = None
    location_raw: str | None = None
    contract_type_raw: str | None = None
    remote_type_raw: str | None = None
    salary_raw: str | None = None
    publication_date_raw: str | None = None
    experience_level_raw: str | None = None
    technologies: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class JobCollector(Protocol):
    """Minimal contract for a source that can return raw job records."""

    source_name: str

    def collect(self) -> list[RawJob]:
        """Collect raw jobs from a source and return them as in-memory data."""
        ...
