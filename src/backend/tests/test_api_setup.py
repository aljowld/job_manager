"""Tests for the FastAPI application setup."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_app_can_be_created() -> None:
    """Test that the FastAPI app is properly instantiated."""
    assert app is not None
    assert app.title == "Job Manager API"


def test_openapi_schema_is_available() -> None:
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema


def test_docs_are_available() -> None:
    """Test that Swagger UI documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_is_available() -> None:
    """Test that ReDoc documentation is accessible."""
    response = client.get("/redoc")
    assert response.status_code == 200
