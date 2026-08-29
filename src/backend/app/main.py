from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app: str


app = FastAPI(
    title="Job Manager API",
    version="0.1.0",
    description="Bootstrap API for the personal job and internship assistant.",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", app="job-manager-backend")
