# GitHub Copilot Instructions

## Project

This repository contains a personal intelligent job and internship search application.

The application is developed incrementally as a modular monolith.

Before making architectural or significant implementation decisions, read:

* `docs/PROJECT_SPEC.md`
* `docs/ARCHITECTURE.md`
* `docs/ROADMAP.md`
* `docs/DEVELOPMENT.md` when relevant

`docs/PROJECT_SPEC.md` defines the product requirements and intended architecture.

`docs/ARCHITECTURE.md` defines the architecture actually adopted by the project and takes precedence for implementation details that have already been decided.

`docs/ROADMAP.md` defines the current development stage and the authorized scope of each step.

Do not silently contradict these documents.

---

## Repository layout

The repository is organized approximately as follows:

```text
/
├── pyproject.toml
├── uv.lock
├── docker-compose.yml
│
├── src/
│   ├── backend/
│   │   ├── app/
│   │   └── tests/
│   │
│   └── frontend/
│       ├── src/
│       └── ...
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

Important paths:

* backend application code: `src/backend/app/`
* backend tests: `src/backend/tests/`
* frontend: `src/frontend/`
* Python project configuration: `pyproject.toml`
* Python lockfile: `uv.lock`

The repository root is the Python project root for:

* `uv`
* Ruff
* ty
* pytest configuration

Python quality commands must therefore normally be executed from the repository root.

Do not recreate obsolete root-level `backend/` or `frontend/` directories.

---

## Development strategy

Develop the application incrementally.

Never implement several major roadmap steps in a single task unless explicitly requested.

For each task:

1. inspect the existing repository first;
2. read the relevant project documentation;
3. identify the current roadmap step;
4. determine the exact scope of the requested work;
5. make the smallest coherent change;
6. add or update appropriate tests;
7. run the required quality checks;
8. update documentation when architecture, configuration, behavior, or roadmap status changes;
9. stop when the requested step is complete.

Do not silently proceed to the next roadmap step.

Do not implement future functionality merely because the current architecture could support it.

If a problem from an earlier step directly blocks the current task, fix only the minimum required and document the reason.

---

## Scope discipline

When given a roadmap step, implement only that step and the minimum supporting changes required for it.

Do not opportunistically implement future functionality.

Before implementing something that appears to belong to a later roadmap step, check `docs/ROADMAP.md`.

If the requested work would materially change the roadmap or architecture:

1. identify the conflict;
2. explain the proposed change;
3. do not silently reorganize the roadmap;
4. document an approved architectural change when appropriate.

Reliability and simplicity take priority over feature count.

---

## Architecture

The application uses a modular monolith architecture.

Do not introduce microservices unless a concrete requirement clearly justifies them.

Main technologies:

* Python;
* FastAPI;
* PostgreSQL;
* SQLAlchemy 2;
* Alembic;
* Pydantic v2;
* React;
* TypeScript;
* Vite.

PostgreSQL is the primary datastore.

Do not introduce without demonstrated need:

* Redis;
* Celery;
* Elasticsearch;
* a separate vector database;
* Kafka or another message broker;
* Kubernetes;
* additional backend services.

Semantic search may later use PostgreSQL with pgvector.

Avoid infrastructure or abstractions that are only justified by hypothetical future scale.

---

## Backend architecture

Backend application code lives in:

```text
src/backend/app/
```

Keep responsibilities separated.

Prefer a pragmatic flow such as:

```text
API
 ↓
Application / service layer
 ↓
Repository when useful
 ↓
SQLAlchemy / PostgreSQL
```

Do not place substantial business logic directly inside FastAPI routes.

Do not create layers purely for architectural ceremony.

Repositories and services should exist only when they make responsibilities clearer.

Avoid generic abstractions such as a large `GenericRepository` unless there is a demonstrated need.

Reuse existing infrastructure instead of creating parallel implementations for:

* configuration;
* SQLAlchemy engine;
* session management;
* dependency injection;
* error handling;
* logging.

---

## Python tooling

Python project management must use Astral `uv`.

Do not use a parallel `pip` + `requirements.txt` workflow unless explicitly justified.

Use:

* `uv` for Python project and dependency management;
* Ruff for application-code linting and formatting;
* ty for static type checking of application code;
* pytest for backend tests.

The project configuration files are at repository root:

```text
pyproject.toml
uv.lock
```

`uv.lock` must be committed to Git.

Never edit `uv.lock` manually.

Python dependencies must be added with commands such as:

```bash
uv add <dependency>
```

Development dependencies should use the appropriate uv dependency mechanism already adopted by the project.

Before adding a dependency, determine whether it is genuinely required.

---

## Backend quality policy

The quality policy intentionally distinguishes application code from tests.

### Application code

```text
src/backend/app/
```

is checked with:

* Ruff linting;
* Ruff formatting;
* ty static type checking.

### Tests

```text
src/backend/tests/
```

are validated with:

* pytest.

Backend tests are intentionally excluded from Ruff and ty.

Do not spend time fixing Ruff formatting, Ruff linting, or ty diagnostics inside `src/backend/tests/` unless explicitly requested.

Do not remove the test exclusions without an explicit project decision.

The expected configuration in `pyproject.toml` should preserve this policy.

Conceptually:

```toml
[tool.ruff]
extend-exclude = ["src/backend/tests"]

[tool.ty.src]
include = ["src/backend/app"]
exclude = ["src/backend/tests"]

[tool.pytest.ini_options]
testpaths = ["src/backend/tests"]
```

Adapt syntax only when required by the actual installed tool versions.

---

## Backend quality gate

Before considering backend work complete, run the relevant checks from the repository root:

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest src/backend/tests
```

If pytest is configured with:

```toml
testpaths = ["src/backend/tests"]
```

then:

```bash
uv run pytest
```

is also acceptable.

Do not claim that a command passed unless it was actually executed successfully.

If a command cannot be executed because of an unavailable external dependency such as Docker or PostgreSQL, state that explicitly.

If the global quality gate reports failures, classify them when relevant as:

1. introduced or affected by the current task;
2. pre-existing and independent of the current task;
3. uncertain and requiring investigation.

Fix failures introduced by the current task.

Do not dismiss an error as pre-existing solely because it appears outside the most obvious file changed by the task.

---

## Python code quality

Write application code that is:

* typed;
* readable;
* modular;
* testable;
* maintainable.

Avoid:

* unnecessary `Any`;
* business logic inside FastAPI routes;
* huge functions;
* huge modules;
* premature abstractions;
* unused abstractions;
* generic repository patterns without demonstrated value;
* duplicated logic;
* unnecessary dependencies;
* silent exception handling;
* broad `except Exception` without a justified technical boundary;
* mutable global state when avoidable.

Prefer clear code over clever code.

Use SOLID principles when they improve maintainability, not as a requirement to create additional layers.

---

## SQLAlchemy and persistence

Use modern SQLAlchemy 2 patterns already established in the project.

Reuse the existing:

* declarative base;
* engine;
* session factory;
* FastAPI database dependency;
* Alembic metadata.

Do not create a second SQLAlchemy engine or session system.

Database schema evolution must use Alembic.

Do not use `Base.metadata.create_all()` as a replacement for Alembic in the normal application startup path.

Use database constraints when they are appropriate for enforcing data integrity.

Important operations affecting multiple related records should remain transactionally coherent.

---

## API design

The API is built with FastAPI.

Business APIs are versioned under:

```text
/api/v1
```

Reuse the existing:

* application factory;
* API router;
* dependency injection;
* centralized exception handling;
* error-response format;
* OpenAPI configuration.

Keep routes thin.

Application and domain services should not depend directly on FastAPI-specific HTTP exceptions unless the HTTP layer genuinely owns the concern.

Prefer:

```text
domain/application error
        ↓
API exception handler
        ↓
HTTP response
```

over embedding HTTP semantics throughout business logic.

Use Pydantic v2 models as explicit API contracts.

Do not expose raw SQLAlchemy models or raw database payloads without a deliberate API schema.

---

## Frontend

Frontend code lives in:

```text
src/frontend/
```

Use:

* React;
* TypeScript in strict mode;
* Vite.

Do not introduce Next.js unless an actual requirement appears.

Prefer feature-oriented organization.

Do not introduce a heavy global state-management library unless a real need appears.

Keep server state and client-only UI state conceptually separate.

Do not implement frontend functionality belonging to a later roadmap step.

---

## Tests

Backend tests live in:

```text
src/backend/tests/
```

Prefer organizing them progressively into concepts such as:

```text
src/backend/tests/
├── unit/
├── integration/
└── fixtures/
```

when this structure becomes useful.

Do not restructure existing tests solely for cosmetic reasons.

Tests should focus primarily on behavior and regressions.

pytest is responsible for validating backend tests.

Ruff and ty intentionally do not validate the test directory.

Automated collector tests must use:

* fixtures;
* mocks;
* recorded/minimal payloads where appropriate.

Tests must not depend directly on live external job websites.

Tests involving PostgreSQL-specific behavior should use PostgreSQL rather than silently substituting SQLite when the database behavior matters.

Add tests for new business logic whenever practical.

When fixing a bug, add or update a regression test when appropriate.

---

## Data collection

Before implementing a real job source:

1. look for an official API;
2. look for RSS, XML, JSON feeds, or another structured interface;
3. review applicable terms and restrictions;
4. inspect `robots.txt` where relevant;
5. determine whether automated access is appropriate;
6. document the chosen collection method.

Never bypass:

* CAPTCHA;
* authentication;
* paywalls;
* anti-bot protections;
* deliberate rate limits;
* technical restrictions intended to prevent automated access.

Prefer the simplest appropriate collection method:

```text
official API
    ↓
structured feed
    ↓
HTTP + parser
    ↓
crawler
    ↓
browser automation only when justified
```

Do not use Playwright when ordinary HTTP is sufficient.

A single failing source must not crash the entire collection process.

Automated tests for sources must not depend on the live source.

---

## Collection architecture

Collection, normalization, deduplication, enrichment, and matching are separate responsibilities.

Preserve a conceptual pipeline similar to:

```text
external source
      ↓
collection
      ↓
raw snapshot
      ↓
parsing
      ↓
normalization
      ↓
canonical candidate
      ↓
deduplication
      ↓
persistence
      ↓
matching
```

Do not put the entire pipeline inside individual scraper implementations.

Source adapters should remain replaceable and isolated from core business logic.

---

## Deduplication

Deduplication must be conservative and non-destructive.

Do not delete source records merely because they appear to be duplicates.

Prefer linking multiple source occurrences to a canonical job offer.

Preserve provenance.

Use strong deterministic signals before fuzzy or semantic similarity.

Ambiguous cases should not be merged aggressively.

Deduplication and user matching are separate concerns:

* deduplication asks whether two records represent the same job;
* matching asks whether a job is relevant to the user.

Do not combine these responsibilities.

---

## Matching

Implement deterministic matching before semantic or LLM-based matching.

Matching must distinguish:

* `MATCH`;
* `MISMATCH`;
* `UNKNOWN`.

Missing information must not automatically be interpreted as a mismatch.

Hard constraints must remain distinguishable from weighted preferences.

Matching results must remain explainable.

A score explanation must be derived from the actual scoring components.

Do not use an LLM to invent a justification after the score has been computed.

The scoring system should eventually be versioned so results can be reproduced and compared.

---

## AI

AI and NLP are post-MVP capabilities unless the roadmap explicitly reaches those steps.

Do not introduce an LLM when deterministic or local processing is sufficient.

Any external AI integration must minimize transmitted personal data.

AI providers should eventually remain replaceable behind appropriate interfaces.

Do not prematurely build abstractions for multiple AI providers before an AI-related roadmap step requires them.

Prefer local, deterministic, and reproducible processing when it adequately solves the problem.

---

## Privacy

Treat as potentially sensitive:

* profile data;
* CV data;
* application history;
* interactions;
* personal preferences.

Do not log sensitive profile contents unnecessarily.

Never log secrets.

Before sending personal information to an external AI service, minimize the payload to the information actually required.

---

## Dependencies

Before adding a dependency:

1. determine whether it is necessary;
2. check whether the standard library already covers the need;
3. check whether an existing project dependency covers the need;
4. avoid overlapping libraries;
5. document dependencies that materially affect the architecture.

Python dependencies must be managed with `uv`.

Do not manually edit `uv.lock`.

Avoid dependencies added only to save a few lines of straightforward code.

---

## Docker

The repository layout must be respected by Docker configuration.

The backend is located at:

```text
src/backend/
```

The frontend is located at:

```text
src/frontend/
```

while:

```text
pyproject.toml
uv.lock
```

are at the repository root.

When modifying Docker configuration, verify:

* build contexts;
* Dockerfile paths;
* `COPY` paths;
* development volumes;
* startup commands;
* access to `pyproject.toml` and `uv.lock`.

Do not assume paths from the previous repository layout.

Do not introduce additional infrastructure services unless the current roadmap step requires them.

---

## Documentation

Update documentation when a task changes:

* architecture;
* repository structure;
* development commands;
* configuration;
* major behavior;
* roadmap status.

Primary documentation:

```text
docs/PROJECT_SPEC.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DEVELOPMENT.md
```

Significant architectural decisions should be recorded as ADRs under:

```text
docs/adr/
```

Create an ADR only for meaningful architectural decisions.

Do not create ADRs for ordinary implementation details.

If repository paths change, update documentation so it reflects the real filesystem.

---

## Roadmap management

`docs/ROADMAP.md` is the source of truth for current development progress.

Do not mark a step as complete unless its essential acceptance criteria are satisfied or remaining limitations are explicitly documented and accepted.

When completing a roadmap step:

1. update only the status of the relevant step;
2. summarize what was actually implemented;
3. record meaningful limitations;
4. do not mark later steps as started;
5. do not silently redefine later steps.

The next roadmap step must not be implemented automatically.

---

## Task completion report

When completing a significant implementation task, report concisely:

1. files created or modified;
2. important implementation decisions;
3. migrations or dependencies added;
4. tests added or updated;
5. commands actually executed;
6. Ruff result for application code;
7. ty result for application code;
8. pytest result;
9. limitations or unresolved pre-existing problems;
10. roadmap status.

Do not claim validation that was not actually performed.

---

## Final engineering principles

When uncertain, prefer:

```text
simple > complex
explicit > implicit
deterministic > opaque
tested > assumed
incremental > large-batch
reversible > destructive
maintainable > clever
```

Do not over-engineer the MVP.

Build the simplest reliable system that satisfies the current roadmap step.
