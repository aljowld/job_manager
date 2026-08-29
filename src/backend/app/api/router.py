"""Main API router with v1 versioning."""

from fastapi import APIRouter

from app.api.routes import health, profile

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health.router)
api_v1_router.include_router(profile.router)
