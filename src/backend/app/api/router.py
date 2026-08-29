"""Main API router with v1 versioning."""

from fastapi import APIRouter

from app.api.routes import health, jobs, profile

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(health.router)
api_v1_router.include_router(profile.router)
api_v1_router.include_router(jobs.router)
