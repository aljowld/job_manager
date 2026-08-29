"""Pydantic schemas for job-offer API responses."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field


class JobSourceOccurrenceSummary(BaseModel):
    """Source provenance for a job offer."""

    id: int
    source_name: str | None = None
    source_url: str | None = None
    external_job_id: str | None = None
    collected_at: datetime | None = None
    is_primary: bool

    model_config = {"from_attributes": True}


class JobOfferSummary(BaseModel):
    """Lightweight representation for a job listing."""

    id: int
    title: str
    company_name: str | None = None
    city: str | None = None
    country: str | None = None
    contract_type: str | None = None
    job_type: str | None = None
    remote_type: str | None = None
    status: str
    publication_date: date | datetime | None = None

    model_config = {"from_attributes": True}


class JobOfferDetail(BaseModel):
    """Detailed representation for a single job offer."""

    id: int
    title: str
    company_name: str | None = None
    company_description: str | None = None
    description: str | None = None
    normalized_description: str | None = None
    job_type: str | None = None
    contract_type: str | None = None
    location_text: str | None = None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    remote_type: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    salary_period: str | None = None
    duration: str | None = None
    experience_level: str | None = None
    education_level: str | None = None
    industry: str | None = None
    job_category: str | None = None
    publication_date: date | datetime | None = None
    expiration_date: date | datetime | None = None
    status: str
    occurrences: list[JobSourceOccurrenceSummary] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class JobOfferListResponse(BaseModel):
    """Paginated list response for offers."""

    page: int
    page_size: int
    total: int
    items: list[JobOfferSummary]

    model_config = {"from_attributes": True}
