from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.dependencies import get_db
from app.factory import create_app


def test_health_endpoint() -> None:
    """Test that the liveness health endpoint responds."""
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_readiness_endpoint_with_database_available() -> None:
    """Test that the readiness endpoint responds ok when database is accessible."""
    app = create_app()
    mock_session = MagicMock()

    def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    response = client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"


def test_readiness_endpoint_with_database_unavailable() -> None:
    """Test that the readiness endpoint handles database unavailability gracefully."""
    app = create_app()
    mock_session = MagicMock()
    mock_session.connection.side_effect = Exception("Connection refused")

    def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    response = client.get("/health/ready")

    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "DATABASE_ERROR"
    assert "Database not accessible" in data["error"]["message"]

