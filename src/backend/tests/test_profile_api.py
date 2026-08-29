"""Tests for the user profile API and persistence."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.dependencies import get_db
from app.db.base import Base
from app.factory import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a test client backed by an in-memory SQLite database."""
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

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_get_profile_when_absent_returns_404(client: TestClient) -> None:
    """Profile should be explicitly absent when it has not been created yet."""
    response = client.get("/api/v1/profile")

    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "PROFILE_NOT_FOUND"
    assert "not been created yet" in data["error"]["message"]


def test_put_profile_creates_and_gets_profile(client: TestClient) -> None:
    """A successful PUT creates a profile and GET returns it back."""
    payload = {
        "full_name": "Alice Durand",
        "email": "alice@example.com",
        "location": "Paris, France",
        "mobility": "3-5km",
        "remote_preference": "hybrid",
        "desired_salary_min": 45000,
        "desired_salary_max": 65000,
        "availability_date": "2026-09-01",
        "internship_duration_weeks": 20,
        "contract_types": [
            {"contract_type": "internship", "preference_level": "REQUIRED"},
            {"contract_type": "cdd", "preference_level": "IMPORTANT"},
        ],
        "job_types": [{"job_type": "full_time", "preference_level": "VERY_IMPORTANT"}],
        "job_roles": [
            {"job_role": "data analyst", "preference_level": "REQUIRED"},
            {"job_role": "business analyst", "preference_level": "BONUS"},
        ],
        "industries": [{"industry": "finance", "preference_level": "IMPORTANT"}],
        "skills": [
            {"skill_name": "SQL", "proficiency_level": "advanced", "years_experience": 4},
            {"skill_name": "Python", "proficiency_level": "advanced", "years_experience": 5},
        ],
        "technologies": [
            {
                "technology_name": "PostgreSQL",
                "proficiency_level": "advanced",
                "years_experience": 3,
            },
            {
                "technology_name": "Power BI",
                "proficiency_level": "intermediate",
                "years_experience": 2,
            },
        ],
        "languages": [
            {"language_name": "French", "proficiency_level": "native"},
            {"language_name": "English", "proficiency_level": "professional"},
        ],
        "preferred_companies": [
            {"company_name": "Mistral AI", "preference_level": "IMPORTANT"},
            {"company_name": "Airbus", "preference_level": "AVOID"},
        ],
    }

    put_response = client.put("/api/v1/profile", json=payload)
    assert put_response.status_code == 200
    saved = put_response.json()
    assert saved["full_name"] == "Alice Durand"
    assert {skill["skill_name"] for skill in saved["skills"]} == {"SQL", "Python"}
    assert {value["contract_type"] for value in saved["contract_types"]} == {"internship", "cdd"}

    get_response = client.get("/api/v1/profile")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "alice@example.com"
    assert len(get_response.json()["languages"]) == 2


def test_put_is_idempotent_and_does_not_duplicate_collections(client: TestClient) -> None:
    """A repeated PUT should keep a single canonical profile without duplicate collections."""
    payload = {
        "full_name": "Alice Durand",
        "skills": [
            {"skill_name": "SQL", "proficiency_level": "advanced", "years_experience": 4},
            {"skill_name": "Python", "proficiency_level": "advanced", "years_experience": 5},
        ],
        "technologies": [
            {
                "technology_name": "PostgreSQL",
                "proficiency_level": "advanced",
                "years_experience": 3,
            },
            {
                "technology_name": "PostgreSQL",
                "proficiency_level": "advanced",
                "years_experience": 3,
            },
        ],
        "languages": [
            {"language_name": "English", "proficiency_level": "professional"},
            {"language_name": "English", "proficiency_level": "professional"},
        ],
        "preferred_companies": [
            {"company_name": "Google", "preference_level": "IMPORTANT"},
            {"company_name": "Google", "preference_level": "IMPORTANT"},
        ],
    }

    first = client.put("/api/v1/profile", json=payload)
    second = client.put("/api/v1/profile", json=payload)

    assert first.status_code == 200
    assert second.status_code == 200
    data = second.json()
    assert len(data["skills"]) == 2
    assert len(data["technologies"]) == 1
    assert len(data["languages"]) == 1
    assert len(data["preferred_companies"]) == 1


def test_invalid_profile_values_are_rejected(client: TestClient) -> None:
    """Validation should reject invalid domain values early."""
    payload = {
        "desired_salary_min": -1,
        "contract_types": [
            {"contract_type": "internship", "preference_level": "NOT_A_VALID_LEVEL"}
        ],
    }

    response = client.put("/api/v1/profile", json=payload)

    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_profile_persists_collection_data(client: TestClient) -> None:
    """The profile persists nested skills, technologies, languages and preferences."""
    payload = {
        "full_name": "Bob Martin",
        "skills": [{"skill_name": "Docker", "proficiency_level": "intermediate", "years_experience": 2}],
        "technologies": [{"technology_name": "FastAPI", "proficiency_level": "advanced", "years_experience": 4}],
        "languages": [{"language_name": "English", "proficiency_level": "professional"}],
        "job_roles": [{"job_role": "backend engineer", "preference_level": "REQUIRED"}],
        "preferred_companies": [{"company_name": "Datadog", "preference_level": "EXCLUDED"}],
    }

    response = client.put("/api/v1/profile", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["skills"][0]["skill_name"] == "Docker"
    assert data["technologies"][0]["technology_name"] == "FastAPI"
    assert data["languages"][0]["language_name"] == "English"
    assert data["job_roles"][0]["preference_level"] == "REQUIRED"
    assert data["preferred_companies"][0]["preference_level"] == "EXCLUDED"
