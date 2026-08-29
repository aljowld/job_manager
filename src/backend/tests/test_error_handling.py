"""Tests for error handling."""

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

from app.core.exceptions import ApplicationError, DatabaseError


def test_application_error_format() -> None:
    """Test that ApplicationError is handled with consistent format."""
    from app.factory import create_app

    app = create_app()

    @app.get("/test-app-error")
    def trigger_app_error() -> None:
        raise ApplicationError("Test error message", "TEST_ERROR")

    client = TestClient(app)
    response = client.get("/test-app-error")

    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "TEST_ERROR"
    assert data["error"]["message"] == "Test error message"


def test_database_error_format() -> None:
    """Test that DatabaseError is handled with consistent format."""
    from app.factory import create_app

    app = create_app()

    @app.get("/test-db-error")
    def trigger_db_error() -> None:
        raise DatabaseError("Connection failed")

    client = TestClient(app)
    response = client.get("/test-db-error")

    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "DATABASE_ERROR"
    assert "Connection failed" in data["error"]["message"]


def test_validation_error_format() -> None:
    """Test that validation errors return consistent format."""
    from app.factory import create_app

    app = create_app()

    @app.get("/test-validation")
    def validation_endpoint(page: int = Query(..., ge=1)) -> dict:
        return {"page": page}

    client = TestClient(app)
    response = client.get("/test-validation?page=invalid")

    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "details" in data["error"]
