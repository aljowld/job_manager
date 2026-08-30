# Job Manager

Personal intelligent job and internship search application.

The goal of the project is to centralize job and internship offers, normalize them, remove duplicates conservatively, compare them against a structured personal profile, rank them with an explainable matching engine, and track job applications.

The project is developed incrementally as a modular monolith.

---

## Current status

Completed roadmap steps:

* ✅ Step 0 — Architecture
* ✅ Step 1 — Repository bootstrap
* ✅ Step 2 — Local Docker/PostgreSQL infrastructure
* ✅ Step 3 — Initial persistence layer
* ✅ Step 4 — FastAPI foundation
* ✅ Step 5 — User profile and preferences
* ✅ Step 6 — Job offer domain and API
* ✅ Step 7 — Fake job collector
* ✅ Step 8 — Collection → normalization → storage pipeline
* ✅ Step 9 — Deduplication

Next authorized step:

* ⬜ Step 10 — First real connector

The detailed roadmap is available in:

```text
docs/ROADMAP.md
```

---

## Main features

The application is being built progressively to support:

* structured personal profile and preferences;
* job collection from authorized sources;
* raw source snapshot preservation;
* job normalization;
* conservative deduplication;
* explainable deterministic matching;
* job ranking and filtering;
* favorites, rejection and archiving;
* application tracking;
* later NLP and semantic search capabilities.

The MVP intentionally does not depend on an LLM.

---

## Architecture

The project uses a modular monolith.

Main components:

* backend: Python + FastAPI;
* database: PostgreSQL;
* persistence: SQLAlchemy 2;
* migrations: Alembic;
* validation/API schemas: Pydantic v2;
* frontend: React + TypeScript + Vite;
* Python dependency management: uv;
* Python linting/formatting: Ruff;
* Python type checking: ty;
* backend tests: pytest;
* local infrastructure: Docker Compose.

Detailed architecture:

```text
docs/ARCHITECTURE.md
```

---

## Repository structure

```text
job_manager/
├── pyproject.toml
├── uv.lock
├── docker-compose.yml
├── .env.example
├── README.md
│
├── src/
│   ├── backend/
│   │   ├── app/
│   │   └── tests/
│   │
│   └── frontend/
│
├── docs/
│   ├── PROJECT_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── DEVELOPMENT.md
│   └── adr/
│
└── .github/
    └── copilot-instructions.md
```

The repository root is the Python project root for:

* uv;
* Ruff;
* ty;
* pytest configuration.

---

## Prerequisites

Recommended local tools:

* Python 3.12;
* uv;
* Node.js 22+;
* npm;
* Docker Desktop or Docker Engine;
* Docker Compose v2;
* Git.

---

## Environment variables

Create the local environment file from the example.

### Linux / macOS

```bash
cp .env.example .env
```

### PowerShell

```powershell
Copy-Item .env.example .env
```

Important variables currently include:

```text
APP_ENV
LOG_LEVEL

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

DATABASE_URL

API_PREFIX

VITE_API_BASE_URL

BACKEND_PORT
FRONTEND_PORT
```

Never commit real secrets.

---

## Python setup

Python dependencies are managed exclusively with uv.

From the repository root:

```bash
uv sync
```

If development dependencies are configured in a dedicated development group:

```bash
uv sync --dev
```

Do not use a parallel `requirements.txt` workflow unless explicitly decided.

---

## Start the full application with Docker

From the repository root:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

Stop the services:

```bash
docker compose down
```

Check service status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Individual services:

```bash
docker compose logs -f postgres
docker compose logs -f backend
docker compose logs -f frontend
```

---

## Run the backend locally

Python commands should be run from the repository root.

Start FastAPI:

```bash
uv run uvicorn app.main:app --app-dir src/backend --reload --host 0.0.0.0 --port 8000
```

The API is then available at:

```text
http://localhost:8000
```

---

## Current backend endpoints

### Health

```text
GET /health
```

### Readiness

```text
GET /health/ready
```

### User profile

```text
GET /api/v1/profile
PUT /api/v1/profile
```

The profile API currently uses a mono-user strategy.

If no profile exists:

```text
GET /api/v1/profile
```

returns:

```text
404 PROFILE_NOT_FOUND
```

`PUT /api/v1/profile` is expected to be idempotent.

---

## API documentation

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

---

## Run the frontend locally

From the repository root:

```bash
cd src/frontend
npm install
npm run dev
```

The default Vite development server is typically available at:

```text
http://localhost:5173
```

Return to the repository root before running Python project commands.

---

## Database migrations

Database schema changes are managed with Alembic.

Apply all migrations:

```bash
uv run alembic upgrade head
```

Inspect current migration state:

```bash
uv run alembic current
```

Create a migration after an intentional SQLAlchemy model change:

```bash
uv run alembic revision --autogenerate -m "description"
```

Always review autogenerated migrations before applying them.

Do not use `Base.metadata.create_all()` as a replacement for normal Alembic migrations.

---

## Backend quality policy

Application code and tests intentionally have different quality responsibilities.

### Application code

```text
src/backend/app/
```

is checked with:

* Ruff lint;
* Ruff formatting;
* ty static type checking.

### Tests

```text
src/backend/tests/
```

are checked with:

* pytest.

Backend tests are intentionally excluded from Ruff and ty.

---

## Backend quality gate

Run from the repository root:

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

Do not consider a task validated merely because targeted tests pass if the task introduced failures elsewhere in the application code.

Pre-existing failures should be distinguished from regressions introduced by the current work.

---

## Tests

Run all backend tests:

```bash
uv run pytest src/backend/tests
```

Concise output:

```bash
uv run pytest src/backend/tests -q
```

Example of a targeted test file:

```bash
uv run pytest src/backend/tests/test_profile_api.py -q
```

Tests for collectors must use fixtures, mocks or recorded payloads and must not depend on live external job websites.

---

## Ruff

Check application code:

```bash
uv run ruff check src/backend/app
```

Check formatting:

```bash
uv run ruff format --check src/backend/app
```

Apply safe fixes preferred during development:

```bash
uv run ruff check src/backend/app --fix
uv run ruff format src/backend/app
```

`--fix` is the preferred automatic correction path for safe Ruff repairs such as unused imports, import ordering, duplicate imports, and other safe fixes. It should not be used as part of the final repository validation gate.

The backend test directory is excluded by project configuration.

---

## ty

Run static type checking:

```bash
uv run ty check
```

The primary type-checked code is:

```text
src/backend/app/
```

Backend tests are intentionally excluded.

---

## Project documentation

Main documentation:

```text
docs/PROJECT_SPEC.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DEVELOPMENT.md
```

Their responsibilities are:

* `PROJECT_SPEC.md` — product requirements and fundamental constraints;
* `ARCHITECTURE.md` — architecture actually adopted;
* `ROADMAP.md` — development steps and current progress;
* `DEVELOPMENT.md` — local development commands and workflows.

Significant architecture decisions are stored under:

```text
docs/adr/
```

---

## Development rules

The project is developed one roadmap step at a time.

Before implementing a step:

1. read `.github/copilot-instructions.md`;
2. read the relevant project documentation;
3. inspect the repository;
4. implement only the current roadmap scope;
5. add appropriate tests;
6. run applicable quality checks;
7. update documentation;
8. stop before the next roadmap step.

Do not implement future functionality opportunistically.

---

## Data collection policy

Before implementing a real source:

1. look for an official API;
2. look for RSS, XML, JSON or another structured feed;
3. review relevant terms and restrictions;
4. inspect `robots.txt` when appropriate;
5. document the chosen collection method.

Never bypass:

* CAPTCHA;
* authentication;
* paywalls;
* anti-bot protections;
* deliberate access restrictions.

Automated source tests must not depend on the live website.

---

## Matching principles

The first matching engine will be deterministic.

It must distinguish:

```text
MATCH
MISMATCH
UNKNOWN
```

Missing information must not automatically be considered a mismatch.

Matching results must remain explainable and reproducible.

LLMs are not required for the MVP matching engine.

---

## Deduplication principles

Deduplication is conservative and non-destructive.

Multiple source occurrences of the same job should remain traceable and be linked to a canonical `JobOffer`.

Source records should not be deleted simply because a duplicate was detected.

---

## MVP boundary

The MVP is reached after roadmap Step 15.

It must support the following flow:

```text
real source
   ↓
collection
   ↓
raw snapshot
   ↓
normalization
   ↓
deduplication
   ↓
canonical job offer
   ↓
deterministic matching
   ↓
ranking
   ↓
frontend consultation
   ↓
favorites / rejection
   ↓
application tracking
```

The MVP must not require:

* LLMs;
* embeddings;
* semantic search;
* Redis;
* Celery;
* machine learning.

---

## Next step

The next authorized roadmap step is:

```text
Step 6 — Job offer domain and API
```

Its goal is to expose already-persisted `JobOffer` records through a typed, paginated and filterable API.

Collection starts only in Step 7.
