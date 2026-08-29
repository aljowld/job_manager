from sqlalchemy import inspect

from app.db.base import Base
from app.db.models import JobOffer, JobSource, JobSourceOccurrence, RawJobSnapshot


def test_core_models_are_registered() -> None:
    model_names = {
        model.__tablename__ for model in (JobSource, RawJobSnapshot, JobOffer, JobSourceOccurrence)
    }

    assert {
        "job_sources",
        "raw_job_snapshots",
        "job_offers",
        "job_source_occurrences",
    } <= model_names


def test_metadata_contains_expected_columns() -> None:
    job_offer_columns = inspect(Base.metadata.tables["job_offers"]).columns.keys()

    assert {"id", "title", "company_name", "description", "created_at", "updated_at"}.issubset(
        job_offer_columns
    )


def test_sqlalchemy_metadata_includes_core_tables() -> None:
    assert {"job_sources", "raw_job_snapshots", "job_offers", "job_source_occurrences"}.issubset(
        Base.metadata.tables.keys()
    )
