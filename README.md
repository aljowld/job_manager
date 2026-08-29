# Job Manager

A personal intelligent job and internship search application.

## Repository status

This repository is currently in the bootstrap phase of the project.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic, Pydantic v2
- Frontend: React, TypeScript, Vite
- Database: PostgreSQL (planned for later stages)
- Tooling: uv, Ruff, ty, pytest

## Quick start

### Backend

```bash
cd src/backend
uv sync --dev
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd src/frontend
npm install
npm run dev
```

## Validation commands

```bash
cd .
uv lock --check
uv run ruff check ./src/backend
uv run ruff format --check ./src/backend
uv run ty check ./src/backend
uv run pytest ./src/backend/tests
```

## Notes

This repository intentionally does not yet implement the business domain, data collection, matching engine, or later roadmap steps. The current work is limited to the Step 1 bootstrap described in the roadmap.
