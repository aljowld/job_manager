# Job Manager

A personal intelligent job and internship search application.

## Repository status

This repository is currently in the bootstrap phase of the project and now includes the local infrastructure configuration for the Step 2 Docker/PostgreSQL setup.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic, Pydantic v2
- Frontend: React, TypeScript, Vite
- Database: PostgreSQL
- Tooling: uv, Ruff, ty, pytest
- Local infrastructure: Docker Compose

## Quick start

### 1. Environment variables

```bash
cp .env.example .env
```

### 2. Start local services with Docker

```bash
docker compose up --build
```

### 3. Stop local services

```bash
docker compose down
```

### Backend local (without Docker)

```bash
cd src/backend
uv sync --dev
uv run uvicorn app.main:app --reload
```

### Frontend local (without Docker)

```bash
cd src/frontend
npm install
npm run dev
```

## Validation commands

```bash
uv lock --check
uv run ruff check ./src/backend
uv run ruff format --check ./src/backend
uv run ty check ./src/backend
uv run pytest ./src/backend/tests
```

## Notes

This repository intentionally does not yet implement the business domain, data collection, matching engine, or later roadmap steps. The current work is limited to the Step 1 bootstrap and the Step 2 local infrastructure setup described in the roadmap.
