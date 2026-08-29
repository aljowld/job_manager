from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint() -> None:
    """Test that the liveness health endpoint responds."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_readiness_endpoint_with_database_unavailable() -> None:
    """Test that the readiness endpoint handles database unavailability gracefully."""
    response = client.get("/health/ready")

    assert response.status_code == 400
    data = response.json()
    assert data["error"]["code"] == "DATABASE_ERROR"
    assert "Database not accessible" in data["error"]["message"]
