"""Health check endpoints."""

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.exceptions import DatabaseError
from fastapi import APIRouter, Depends

router = APIRouter(tags=["health"])


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str


class ReadinessResponse(BaseModel):
    """Response model for readiness check."""

    status: str
    database: str


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Liveness check: indicates the application HTTP layer is running.

    Returns:
        HealthResponse with status "ok".
    """
    return HealthResponse(status="ok")


@router.get("/health/ready", response_model=ReadinessResponse)
def readiness_check(db: Session = Depends(get_db)) -> ReadinessResponse:
    """Readiness check: verifies the application and database are ready to serve traffic.

    Args:
        db: Database session from dependency injection.

    Returns:
        ReadinessResponse with status and database connectivity.

    Raises:
        DatabaseError: If database is not accessible.
    """
    try:
        db.connection()
        database_status = "ok"
    except Exception as e:
        raise DatabaseError(f"Database not accessible: {str(e)}") from e

    return ReadinessResponse(status="ok", database=database_status)
