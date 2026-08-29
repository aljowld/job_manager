"""Tests for the jobs listing and detail API."""

from __future__ import annotations

from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.db.base import Base
from app.db.models import JobOffer, JobSource, JobSourceOccurrence
from app.factory import create_app


def _create_test_client(seed_data: bool = True) -> TestClient:
    """Create a client with optional seeded offer data for deterministic route tests."""
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

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    if seed_data:
        with TestClient(app) as test_client:
            db = TestingSessionLocal()
            source_1 = JobSource(name="Greenhouse", base_url="https://example.com", enabled=True)
            source_2 = JobSource(name="Lever", base_url="https://lever.example.com", enabled=True)
            db.add_all([source_1, source_2])
            db.flush()

            offers = [
                JobOffer(
                    title="Backend Engineer",
                    company_name="Acme",
                    city="Paris",
                    country="FR",
                    contract_type="CDI",
                    job_type="full_time",
                    remote_type="hybrid",
                    status="active",
                    publication_date=datetime(2026, 1, 10, tzinfo=UTC),
                    created_at=datetime(2026, 1, 1, tzinfo=UTC),
                    updated_at=datetime(2026, 1, 1, tzinfo=UTC),
                    description="Build backend services.",
                ),
                JobOffer(
                    title="Data Analyst",
                    company_name="Acme",
                    city="Lyon",
                    country="FR",
                    contract_type="CDD",
                    job_type="full_time",
                    remote_type="remote",
                    status="active",
                    publication_date=datetime(2026, 1, 15, tzinfo=UTC),
                    created_at=datetime(2026, 1, 2, tzinfo=UTC),
                    updated_at=datetime(2026, 1, 2, tzinfo=UTC),
                    description="Analyze data pipelines.",
                ),
                JobOffer(
                    title="Product Designer",
                    company_name="Beta",
                    city="Berlin",
                    country="DE",
                    contract_type="internship",
                    job_type="part_time",
                    remote_type="on_site",
                    status="archived",
                    publication_date=datetime(2025, 12, 20, tzinfo=UTC),
                    created_at=datetime(2025, 12, 1, tzinfo=UTC),
                    updated_at=datetime(2025, 12, 1, tzinfo=UTC),
                    description="Design product flows.",
                ),
            ]
            db.add_all(offers)
            db.flush()

            db.add_all(
                [
                    JobSourceOccurrence(
                        job_offer_id=offers[0].id,
                        source_id=source_1.id,
                        external_job_id="gh-100",
                        source_url="https://example.com/jobs/100",
                        is_primary=True,
                        status="active",
                        collected_at=datetime(2026, 1, 11, tzinfo=UTC),
                    ),
                    JobSourceOccurrence(
                        job_offer_id=offers[1].id,
                        source_id=source_2.id,
                        external_job_id="lev-200",
                        source_url="https://lever.example.com/jobs/200",
                        is_primary=True,
                        status="active",
                        collected_at=datetime(2026, 1, 16, tzinfo=UTC),
                    ),
                ]
            )
            db.commit()
            db.close()
            return test_client

    return TestClient(app)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a test client with seeded job data."""
    app = create_app()
    test_client = _create_test_client(seed_data=True)
    yield test_client
    test_client.app.dependency_overrides.clear()


@pytest.fixture()
def empty_client() -> Generator[TestClient, None, None]:
    """Provide an empty test client for empty-list assertions."""
    test_client = _create_test_client(seed_data=False)
    yield test_client
    test_client.app.dependency_overrides.clear()


def test_jobs_list_is_empty_when_no_offers_exist(empty_client: TestClient) -> None:
    """Listing offers returns an empty result with pagination metadata when there are none."""
    response = empty_client.get("/api/v1/jobs")

    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 1
    assert payload["page_size"] == 20
    assert payload["total"] == 0
    assert payload["items"] == []


def test_jobs_list_supports_pagination_and_filters(client: TestClient) -> None:
    """The jobs list endpoint supports pagination, filters and a deterministic sort."""
    response = client.get(
        "/api/v1/jobs",
        params={
            "company_name": "Acme",
            "country": "FR",
            "page": 1,
            "page_size": 1,
            "sort_by": "publication_date",
            "sort_order": "desc",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 1
    assert payload["page_size"] == 1
    assert payload["total"] == 2
    assert len(payload["items"]) == 1
    assert payload["items"][0]["title"] == "Data Analyst"


def test_jobs_list_respects_page_size_limit(client: TestClient) -> None:
    """The maximum page size is enforced automatically."""
    response = client.get("/api/v1/jobs", params={"page_size": 999})

    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_jobs_detail_returns_offer_and_origin(client: TestClient) -> None:
    """The job detail endpoint exposes the canonical offer and source provenance."""
    response = client.get("/api/v1/jobs/1")

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["title"] == "Backend Engineer"
    assert payload["company_name"] == "Acme"
    assert payload["occurrences"][0]["source_name"] == "Greenhouse"
    assert payload["occurrences"][0]["external_job_id"] == "gh-100"


def test_jobs_detail_returns_404_for_missing_offer(client: TestClient) -> None:
    """A missing offer returns a dedicated application error."""
    response = client.get("/api/v1/jobs/999")

    assert response.status_code == 404
    payload = response.json()
    assert payload["error"]["code"] == "JOB_OFFER_NOT_FOUND"


def test_jobs_list_supports_sorting_by_title(client: TestClient) -> None:
    """The list endpoint supports a closed-sort field set and deterministic ordering."""
    response = client.get("/api/v1/jobs", params={"sort_by": "title", "sort_order": "asc"})

    assert response.status_code == 200
    titles = [item["title"] for item in response.json()["items"]]
    assert titles == ["Backend Engineer", "Data Analyst", "Product Designer"]
