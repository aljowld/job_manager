# Développement local

## Prérequis

- Docker Desktop ou Docker Engine
- Docker Compose v2
- Python 3.12
- uv
- Node.js 22+

## Variables d’environnement

Copiez le fichier d’exemple et adaptez les valeurs si nécessaire :

```bash
cp .env.example .env
```

Variables essentielles :

- `APP_ENV`
- `LOG_LEVEL`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_PORT`
- `POSTGRES_HOST`
- `DATABASE_URL`
- `API_PREFIX`
- `VITE_API_BASE_URL`
- `BACKEND_PORT`
- `FRONTEND_PORT`

Les valeurs du fichier `.env` ne doivent pas contenir de secrets réels ou sensibles dans le dépôt partagé.

## Démarrage local avec Docker

```bash
docker compose up --build
```

Pour arrêter les services :

```bash
docker compose down
```

Pour reconstruire sans cache :

```bash
docker compose build --no-cache
```

## Vérification des services

```bash
docker compose ps
docker compose logs -f postgres
docker compose logs -f backend
docker compose logs -f frontend
```

## Backend local

```bash
cd src/backend
uv sync --dev
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`:
- REST API: `http://localhost:8000/api/v1`
- OpenAPI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`
- Readiness check: `http://localhost:8000/health/ready`

## Frontend local

```bash
cd src/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Qualité backend

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

Les dépendances Python du backend doivent rester gérées par uv et reflétées dans le lockfile, sans workflow parallèle basé sur requirements.txt.

## Remarque sur le runtime Docker

Ce dépôt a été configuré pour un workflow local Docker simple. Le lancement réel des conteneurs a été bloqué dans cet environnement parce que Docker n’était pas installé. La configuration YAML et les fichiers de build ont néanmoins été préparés pour un démarrage local reproductible après installation de Docker.
