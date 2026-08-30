"""Integration test: Arbeitnow connector feeding the existing collection pipeline."""

from __future__ import annotations

from collections.abc import Generator

import httpx
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.collection.arbeitnow import ArbeitnowJobSource
from app.collection.pipeline import CollectionPipeline
from app.db.base import Base
from app.db.models import JobOffer, JobSource, JobSourceOccurrence, RawJobSnapshot


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def _arbeitnow_source_with_fixture(job_slug: str = "backend-engineer-berlin-1") -> ArbeitnowJobSource:
    def handler(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        if page > 1:
            return httpx.Response(200, json={"data": []})
        return httpx.Response(
            200,
            json={
                "data": [
                    {
                        "slug": job_slug,
                        "company_name": "Acme GmbH",
                        "title": "Backend Engineer",
                        "description": "<p>Build APIs.</p>",
                        "remote": True,
                        "url": f"https://www.arbeitnow.com/jobs/companies/acme/{job_slug}",
                        "tags": ["python"],
                        "job_types": ["Experienced", "Full time"],
                        "location": "Berlin",
                        "created_at": 1788000000,
                    }
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    return ArbeitnowJobSource(client=client, max_pages=2)


def test_arbeitnow_source_persists_through_the_existing_pipeline(db_session: Session) -> None:
    pipeline = CollectionPipeline(db_session)
    source = _arbeitnow_source_with_fixture()

    result = pipeline.run(source)

    assert result.collected == 1
    assert result.persisted == 1
    assert db_session.query(JobSource).filter_by(name="arbeitnow").count() == 1
    assert db_session.query(RawJobSnapshot).count() == 1
    assert db_session.query(JobOffer).count() == 1

    occurrence = db_session.query(JobSourceOccurrence).one()
    assert occurrence.source.name == "arbeitnow"
    assert occurrence.external_job_id == "backend-engineer-berlin-1"
    assert occurrence.source_url == "https://www.arbeitnow.com/jobs/companies/acme/backend-engineer-berlin-1"


def test_arbeitnow_recollection_does_not_create_a_duplicate_canonical_offer(db_session: Session) -> None:
    pipeline = CollectionPipeline(db_session)

    first = pipeline.run(_arbeitnow_source_with_fixture())
    second = pipeline.run(_arbeitnow_source_with_fixture())

    assert first.persisted == 1
    assert second.persisted == 1
    assert db_session.query(JobOffer).count() == 1
    assert db_session.query(JobSourceOccurrence).count() == 1
    assert db_session.query(RawJobSnapshot).count() == 2
