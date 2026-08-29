# AGENTS.md

## Project

This repository contains a personal intelligent job and internship search application.

Before making architectural or significant implementation decisions, read:

* `docs/PROJECT_SPEC.md`
* `docs/ARCHITECTURE.md`
* `docs/ROADMAP.md`
* `docs/DEVELOPMENT.md` when available

`docs/PROJECT_SPEC.md` defines the product requirements and intended architecture.

`docs/ARCHITECTURE.md` defines the architecture actually adopted by the project and takes precedence for already-decided implementation details.

## Development strategy

Develop the application incrementally.

Never implement several major roadmap steps in a single task unless explicitly requested.

For each task:

1. inspect the existing repository first;
2. identify the current roadmap step;
3. make the smallest coherent change;
4. add or update tests;
5. run the required quality checks;
6. update documentation when architecture or behavior changes;
7. stop when the requested step is complete.

Do not silently proceed to the next roadmap step.

## Architecture

The initial architecture is a modular monolith.

Do not introduce microservices unless a concrete requirement justifies them.

Main components:

* Python / FastAPI backend;
* PostgreSQL;
* SQLAlchemy 2;
* Alembic;
* Pydantic v2;
* React;
* TypeScript;
* Vite.

Prefer PostgreSQL as the primary datastore.

Do not introduce Redis, Celery, Elasticsearch, or a separate vector database without a demonstrated need.

Semantic search may later use PostgreSQL + pgvector.

## Python tooling

Python project management must use Astral `uv`.

Do not use a parallel pip/requirements.txt workflow unless explicitly justified.

Use:

* `uv` for Python project and dependency management;
* `ruff` for linting and formatting;
* `ty` for static type checking;
* `pytest` for backend tests.

The Python lockfile `uv.lock` must be committed.

Never edit `uv.lock` manually.

## Backend quality gate

Before considering backend work complete, run the relevant checks:

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

If a command fails because the project is not yet at the stage where it exists, state that explicitly.

Do not claim checks passed unless they were actually executed successfully.

## Python code quality

Write typed, readable, modular code.

Avoid:

* unnecessary `Any`;
* business logic inside FastAPI routes;
* huge functions or files;
* premature abstractions;
* generic repository abstractions without real value;
* duplicated logic;
* unnecessary dependencies;
* silent exception handling.

Use domain-oriented services and repositories where they clarify responsibilities.

## Frontend

Use:

* React;
* TypeScript in strict mode;
* Vite.

Do not introduce Next.js unless an actual requirement appears.

Prefer feature-oriented organization.

Do not add a heavy global state library unless necessary.

## Data collection

Before implementing a real job source:

1. look for an official API;
2. look for RSS or structured feeds;
3. review applicable terms and restrictions;
4. inspect robots.txt where relevant;
5. document the chosen collection method.

Never bypass:

* CAPTCHA;
* authentication;
* paywalls;
* anti-bot protections;
* deliberate rate limits.

A single failing source must not crash the entire collection system.

## Matching

Implement deterministic matching before semantic or LLM-based matching.

Distinguish:

* MATCH;
* MISMATCH;
* UNKNOWN.

Missing data must not automatically be interpreted as a mismatch.

Matching results must remain explainable.

Do not use an LLM to invent score explanations.

## Deduplication

Deduplication must be conservative and non-destructive.

Do not delete duplicate source records.

Prefer linking multiple source occurrences to a canonical job offer.

## AI

Do not use an LLM when deterministic or local processing is sufficient.

Any external AI integration must minimize transmitted personal data.

AI providers must eventually remain replaceable.

## Tests

Automated collector tests must use fixtures, recorded payloads, or mocks.

Tests must not depend on live external job websites.

Add tests for new business logic whenever practical.

## Dependencies

Before adding a dependency:

1. determine whether it is necessary;
2. check whether the standard library or an existing dependency already covers the need;
3. avoid overlapping libraries;
4. document significant dependencies.

Python dependencies must be added using `uv`.

## Documentation

Update documentation when a task changes:

* architecture;
* development commands;
* configuration;
* major behavior;
* roadmap status.

Significant architecture decisions should be recorded as ADRs under:

`docs/adr/`

## Scope discipline

When given a roadmap step, implement only that step and the minimum supporting changes required for it.

Do not opportunistically implement future functionality.

Reliability and simplicity take priority over feature count.
