"""Routes for consulting persisted job offers."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.exceptions import ApplicationError
from app.db.models import JobOffer, JobSourceOccurrence
from app.schemas.jobs import JobOfferDetail, JobOfferListResponse, JobOfferSummary

router = APIRouter(tags=["jobs"])

ALLOWED_SORT_FIELDS = {
    "publication_date": JobOffer.publication_date,
    "created_at": JobOffer.created_at,
    "title": JobOffer.title,
}

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 20


class JobOfferNotFoundError(ApplicationError):
    """Raised when a requested job offer does not exist."""

    def __init__(self, offer_id: int) -> None:
        super().__init__(f"Job offer #{offer_id} was not found", "JOB_OFFER_NOT_FOUND", 404)


def _build_sort_expression(sort_by: str, sort_order: str):
    """Build a deterministic SQLAlchemy sort expression from a closed allow-list."""
    column = ALLOWED_SORT_FIELDS.get(sort_by)
    if column is None:
        raise ValueError(f"Unsupported sort field: {sort_by}")
    return asc(column) if sort_order == "asc" else desc(column)


def _apply_filters(params: dict[str, str | None]) -> list:
    """Apply allowed filters and return a list of SQLAlchemy conditions."""
    filters: list = []
    if params.get("company_name"):
        filters.append(JobOffer.company_name.ilike(f"%{params['company_name']}%"))
    if params.get("city"):
        filters.append(JobOffer.city.ilike(f"%{params['city']}%"))
    if params.get("country"):
        filters.append(JobOffer.country.ilike(f"%{params['country']}%"))
    if params.get("contract_type"):
        filters.append(JobOffer.contract_type == params["contract_type"])
    if params.get("job_type"):
        filters.append(JobOffer.job_type == params["job_type"])
    if params.get("remote_type"):
        filters.append(JobOffer.remote_type == params["remote_type"])
    if params.get("status"):
        filters.append(JobOffer.status == params["status"])
    if params.get("publication_date_from"):
        filters.append(JobOffer.publication_date >= params["publication_date_from"])
    if params.get("publication_date_to"):
        filters.append(JobOffer.publication_date <= params["publication_date_to"])
    return filters


@router.get("/jobs", response_model=JobOfferListResponse)
def list_jobs(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE),
    company_name: str | None = None,
    city: str | None = None,
    country: str | None = None,
    contract_type: str | None = None,
    job_type: str | None = None,
    remote_type: str | None = None,
    status: str | None = None,
    publication_date_from: str | None = None,
    publication_date_to: str | None = None,
    sort_by: str = Query("publication_date", pattern="^(publication_date|created_at|title)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$"),
) -> JobOfferListResponse:
    """Return a paginated, filterable list of job offers."""
    params = {
        "company_name": company_name,
        "city": city,
        "country": country,
        "contract_type": contract_type,
        "job_type": job_type,
        "remote_type": remote_type,
        "status": status,
        "publication_date_from": publication_date_from,
        "publication_date_to": publication_date_to,
    }

    filters = _apply_filters(params)
    total_query = select(func.count()).select_from(JobOffer)
    if filters:
        total_query = total_query.where(*filters)
    total = db.scalar(total_query) or 0

    query = select(JobOffer)
    if filters:
        query = query.where(*filters)

    sort_expression = _build_sort_expression(sort_by, sort_order)
    query = query.order_by(sort_expression, JobOffer.id.asc())
    items = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()

    return JobOfferListResponse(
        page=page,
        page_size=page_size,
        total=total,
        items=[
            JobOfferSummary(
                id=item.id,
                title=item.title,
                company_name=item.company_name,
                city=item.city,
                country=item.country,
                contract_type=item.contract_type,
                job_type=item.job_type,
                remote_type=item.remote_type,
                status=item.status,
                publication_date=item.publication_date,
            )
            for item in items
        ],
    )


@router.get("/jobs/{job_id}", response_model=JobOfferDetail)
def get_job_offer(job_id: int, db: Session = Depends(get_db)) -> JobOfferDetail:
    """Return the canonical details of a single persisted job offer."""
    offer = db.get(JobOffer, job_id)
    if offer is None:
        raise JobOfferNotFoundError(job_id)

    occurrences = (
        db.query(JobSourceOccurrence)
        .filter(JobSourceOccurrence.job_offer_id == offer.id)
        .order_by(JobSourceOccurrence.is_primary.desc(), JobSourceOccurrence.collected_at.desc())
        .all()
    )

    return JobOfferDetail(
        id=offer.id,
        title=offer.title,
        company_name=offer.company_name,
        company_description=offer.company_description,
        description=offer.description,
        normalized_description=offer.normalized_description,
        job_type=offer.job_type,
        contract_type=offer.contract_type,
        location_text=offer.location_text,
        city=offer.city,
        region=offer.region,
        country=offer.country,
        remote_type=offer.remote_type,
        salary_min=offer.salary_min,
        salary_max=offer.salary_max,
        salary_currency=offer.salary_currency,
        salary_period=offer.salary_period,
        duration=offer.duration,
        experience_level=offer.experience_level,
        education_level=offer.education_level,
        industry=offer.industry,
        job_category=offer.job_category,
        publication_date=offer.publication_date,
        expiration_date=offer.expiration_date,
        status=offer.status,
        occurrences=[
            {
                "id": occurrence.id,
                "source_name": occurrence.source.name if occurrence.source else None,
                "source_url": occurrence.source_url,
                "external_job_id": occurrence.external_job_id,
                "collected_at": occurrence.collected_at,
                "is_primary": occurrence.is_primary,
            }
            for occurrence in occurrences
        ],
    )
