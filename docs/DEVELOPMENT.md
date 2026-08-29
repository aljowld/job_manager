# Développement local

Ce document décrit l'installation, le lancement et les commandes de développement du projet.

La structure principale du repository est :

```text
job_manager/
├── pyproject.toml
├── uv.lock
├── docker-compose.yml
├── .env.example
│
├── src/
│   ├── backend/
│   │   ├── app/
│   │   └── tests/
│   │
│   └── frontend/
│
├── docs/
└── .github/
```

Le **repository root** est la racine du projet Python pour :

* uv ;
* Ruff ;
* ty ;
* pytest.

Les commandes Python décrites dans ce document doivent donc être exécutées depuis la racine du repository, sauf indication contraire.

---

# 1. Prérequis

Pour travailler sur le projet localement :

* Python 3.12 ;
* uv ;
* Node.js 22+ ;
* npm ;
* Docker Desktop ou Docker Engine ;
* Docker Compose v2 ;
* Git.

Docker est nécessaire pour le workflow local complet avec PostgreSQL.

Le backend Python peut néanmoins être exécuté directement avec uv lorsque PostgreSQL est disponible.

---

# 2. Variables d'environnement

À partir de la racine du repository, créer le fichier `.env` depuis le modèle :

## Linux / macOS

```bash
cp .env.example .env
```

## PowerShell

```powershell
Copy-Item .env.example .env
```

Adapter ensuite les valeurs si nécessaire.

Variables actuellement importantes :

```text
APP_ENV
LOG_LEVEL

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_PORT
POSTGRES_HOST

DATABASE_URL

API_PREFIX

VITE_API_BASE_URL

BACKEND_PORT
FRONTEND_PORT
```

Toutes les variables futures ne doivent être ajoutées que lorsqu'une fonctionnalité en a réellement besoin.

Le fichier :

```text
.env
```

ne doit jamais être versionné.

Le fichier :

```text
.env.example
```

ne doit contenir que des valeurs d'exemple non sensibles.

---

# 3. Installation des dépendances Python

Les dépendances Python sont gérées exclusivement avec **uv**.

Les fichiers de référence sont situés à la racine :

```text
pyproject.toml
uv.lock
```

Depuis la racine du repository :

```bash
uv sync
```

Si le projet utilise explicitement un groupe de développement séparé nécessitant cette option :

```bash
uv sync --dev
```

Ne pas mettre en place parallèlement un workflow basé sur :

```text
requirements.txt
pip install -r ...
```

sauf décision explicite du projet.

---

# 4. Ajouter une dépendance Python

Depuis la racine :

```bash
uv add <package>
```

Pour une dépendance de développement, utiliser le mécanisme de groupe de dépendances déjà retenu dans `pyproject.toml`.

Exemple conceptuel :

```bash
uv add --dev <package>
```

Ne jamais modifier `uv.lock` manuellement.

Après une modification des dépendances :

```bash
uv lock --check
```

doit rester valide.

---

# 5. Démarrage complet avec Docker

Depuis la racine du repository :

```bash
docker compose up --build
```

Cette commande doit démarrer au minimum :

```text
postgres
backend
frontend
```

Pour lancer les services en arrière-plan :

```bash
docker compose up --build -d
```

Pour arrêter les services :

```bash
docker compose down
```

Pour arrêter les services et supprimer les conteneurs sans supprimer volontairement les données persistantes :

```bash
docker compose down
```

Ne supprimer les volumes PostgreSQL que lorsqu'une réinitialisation complète de la base est réellement souhaitée.

---

# 6. Reconstruction Docker

Pour reconstruire les images :

```bash
docker compose build
```

Pour reconstruire sans utiliser le cache :

```bash
docker compose build --no-cache
```

Puis :

```bash
docker compose up
```

---

# 7. Vérification des services Docker

Afficher l'état des services :

```bash
docker compose ps
```

Consulter les logs PostgreSQL :

```bash
docker compose logs -f postgres
```

Consulter les logs backend :

```bash
docker compose logs -f backend
```

Consulter les logs frontend :

```bash
docker compose logs -f frontend
```

Afficher tous les logs :

```bash
docker compose logs -f
```

---

# 8. Backend local sans conteneur applicatif

Le projet Python est piloté depuis la racine.

Ne pas exécuter uv depuis :

```text
src/backend/
```

Le backend FastAPI se trouve dans :

```text
src/backend/app/
```

Pour lancer FastAPI depuis la racine du repository, utiliser la commande correspondant à la structure réelle du projet.

Avec l'organisation actuelle :

```bash
uv run uvicorn app.main:app --app-dir src/backend --reload --host 0.0.0.0 --port 8000
```

Cette commande indique explicitement à Uvicorn que le module `app` se trouve dans :

```text
src/backend/
```

Le backend doit alors être disponible sur :

```text
http://localhost:8000
```

---

# 9. Endpoints techniques actuels

## Santé

```text
GET http://localhost:8000/health
```

## Readiness

```text
GET http://localhost:8000/health/ready
```

Le readiness check vérifie notamment la disponibilité nécessaire de PostgreSQL.

## API versionnée

Base de l'API métier :

```text
http://localhost:8000/api/v1
```

## Profil utilisateur

```text
GET http://localhost:8000/api/v1/profile
PUT http://localhost:8000/api/v1/profile
```

## Offres d'emploi

```text
GET http://localhost:8000/api/v1/jobs
GET http://localhost:8000/api/v1/jobs/{id}
```

Les offres peuvent être paginées et filtrées selon les champs réellement présents dans le modèle `JobOffer`.

## Documentation OpenAPI

Swagger UI :

```text
http://localhost:8000/docs
```

ReDoc :

```text
http://localhost:8000/redoc
```

Schéma OpenAPI :

```text
http://localhost:8000/openapi.json
```

---

# 10. Comportement actuel du profil

L'API de profil fonctionne actuellement en mode **mono-utilisateur**.

Un seul profil actif est géré par l'application.

Lecture :

```text
GET /api/v1/profile
```

Si aucun profil n'existe encore, l'API retourne une erreur :

```text
404 PROFILE_NOT_FOUND
```

Création ou remplacement :

```text
PUT /api/v1/profile
```

Le `PUT` est conçu pour être idempotent.

Deux requêtes identiques doivent produire le même état final sans créer de doublons dans les relations associées au profil.

La mise à jour des données liées au profil doit rester transactionnelle.

---

# 11. PostgreSQL local

Le moyen recommandé pour le développement est d'utiliser PostgreSQL via Docker Compose.

Le service PostgreSQL est accessible aux autres conteneurs via son nom de service Docker, généralement :

```text
postgres
```

Attention à la différence entre :

```text
localhost
```

et :

```text
postgres
```

## Backend exécuté depuis la machine hôte

Lorsque FastAPI tourne directement avec uv sur la machine, PostgreSQL exposé par Docker est généralement joint via :

```text
localhost:<POSTGRES_PORT>
```

## Backend exécuté dans Docker

Lorsque FastAPI tourne lui-même dans Docker Compose, le hostname PostgreSQL doit utiliser le nom du service Docker :

```text
postgres
```

La valeur effective de `DATABASE_URL` doit donc rester cohérente avec le mode d'exécution utilisé.

Ne pas coder ces valeurs directement dans le code Python.

---

# 12. Alembic

Les migrations de base de données sont gérées avec Alembic.

Ne pas utiliser `Base.metadata.create_all()` comme remplacement du système de migrations dans le fonctionnement normal de l'application.

## Voir l'état actuel

Depuis la racine :

```bash
uv run alembic current
```

## Appliquer toutes les migrations

```bash
uv run alembic upgrade head
```

## Créer une nouvelle migration

Après modification volontaire des modèles SQLAlchemy :

```bash
uv run alembic revision --autogenerate -m "description"
```

Toujours relire une migration générée automatiquement avant de l'appliquer.

## Revenir d'une migration

Lorsque cela est approprié et sans risque sur des données importantes :

```bash
uv run alembic downgrade -1
```

Puis réappliquer :

```bash
uv run alembic upgrade head
```

Ne pas modifier rétroactivement une ancienne migration déjà considérée comme appliquée simplement pour ajouter une nouvelle fonctionnalité.

Créer une nouvelle migration.

---

# 13. Frontend local

Le frontend est situé dans :

```text
src/frontend/
```

Depuis la racine :

```bash
cd src/frontend
```

Installer les dépendances :

```bash
npm install
```

Puis lancer Vite :

```bash
npm run dev -- --host 0.0.0.0 --port 5173
```

Le frontend doit alors être disponible sur :

```text
http://localhost:5173
```

Après le travail frontend, revenir à la racine avant d'exécuter les commandes uv :

```bash
cd ../..
```

Sous PowerShell :

```powershell
Set-Location ../..
```

---

# 14. Politique de qualité backend

La politique qualité distingue volontairement le code applicatif des tests.

## Code applicatif

Le code situé dans :

```text
src/backend/app/
```

est vérifié avec :

* Ruff lint ;
* Ruff format ;
* ty.

## Tests

Les tests situés dans :

```text
src/backend/tests/
```

sont vérifiés avec :

* pytest.

Ils sont volontairement exclus de Ruff et ty.

Cette décision évite de consacrer inutilement du temps au typage ou au style de :

* mocks ;
* fixtures ;
* monkeypatches ;
* helpers propres aux tests.

Le comportement des tests reste la priorité.

---

# 15. Quality gate backend

Depuis la racine du repository :

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

La répartition est :

```text
src/backend/app/     → Ruff + Ruff format + ty
src/backend/tests/   → pytest
```

Si pytest est configuré avec :

```toml
[tool.pytest.ini_options]
testpaths = ["src/backend/tests"]
```

la commande suivante est également suffisante :

```bash
uv run pytest
```

---

# 16. Ruff

Vérification :

```bash
uv run ruff check src/backend/app
```

Correction automatique des problèmes sûrs, privilégiée pendant le développement :

```bash
uv run ruff check src/backend/app --fix
uv run ruff format src/backend/app
```

`--fix` doit être présenté comme la méthode privilégiée pour corriger automatiquement les violations sûres lorsque Ruff le permet, notamment :

* imports inutilisés ;
* ordre et regroupement des imports ;
* imports dupliqués ;
* autres corrections automatiques sûres proposées par Ruff.

Vérification du formatage :

```bash
uv run ruff format --check src/backend/app
```

Le dossier :

```text
src/backend/tests/
```

doit rester exclu selon la configuration du projet.

Ruff ne doit donc pas être utilisé pour reformater les tests sauf décision explicite contraire.

---

# 17. ty

La vérification statique du code applicatif est effectuée avec :

```bash
uv run ty check
```

Le périmètre principal est :

```text
src/backend/app/
```

Le dossier :

```text
src/backend/tests/
```

est volontairement exclu.

Les suppressions de type ou usages de `Any` dans le code applicatif doivent rester limités et justifiés.

---

# 18. pytest

Lancer tous les tests backend :

```bash
uv run pytest src/backend/tests
```

Mode concis :

```bash
uv run pytest src/backend/tests -q
```

Lancer un fichier spécifique :

```bash
uv run pytest src/backend/tests/test_profile_api.py -q
```

Lancer un test spécifique :

```bash
uv run pytest src/backend/tests/test_profile_api.py::nom_du_test -q
```

Lorsqu'un bug est corrigé, ajouter ou maintenir un test de régression lorsque cela est pertinent.

---

# 19. Organisation future des tests

Les tests backend peuvent progressivement être organisés ainsi :

```text
src/backend/tests/
├── unit/
├── integration/
├── fixtures/
└── conftest.py
```

Cette réorganisation ne doit être réalisée que lorsqu'elle améliore réellement la lisibilité.

## Tests unitaires

Pour :

* services purs ;
* validations ;
* normalisation ;
* matching ;
* déduplication ;
* utilitaires métier.

## Tests d'intégration

Pour :

* FastAPI ;
* PostgreSQL ;
* repositories ;
* migrations ;
* transactions ;
* pipeline de collecte.

## Fixtures

Pour :

* offres fictives ;
* HTML ;
* JSON ;
* XML ;
* données de sources ;
* scénarios reproductibles.

Les tests de collecteurs ne doivent pas dépendre de sites externes réels.

---

# 20. Workflow conseillé avant un commit backend

Depuis la racine :

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

Pendant le développement, les corrections sûres peuvent être appliquées automatiquement avec :

```bash
uv run ruff check src/backend/app --fix
uv run ruff format src/backend/app
```

Puis relancer le quality gate sans utiliser `--fix` dans la validation finale.

Vérifier ensuite les modifications Git :

```bash
git status
git diff
```

Puis créer le commit uniquement après revue des changements.

---

# 21. Workflow conseillé pour une étape de roadmap

Chaque étape doit suivre approximativement :

```text
Lire la documentation
        ↓
Inspecter le repository
        ↓
Implémenter uniquement l'étape courante
        ↓
Ajouter les tests
        ↓
Exécuter les quality gates
        ↓
Corriger les régressions
        ↓
Mettre à jour ROADMAP.md
        ↓
Revue git diff
        ↓
Commit
```

Ne pas commencer automatiquement l'étape suivante.

---

# 22. Gestion des erreurs préexistantes

Si un quality gate échoue, distinguer :

1. une erreur introduite ou affectée par le travail courant ;
2. une erreur préexistante et indépendante ;
3. une erreur dont l'origine est incertaine.

Toute erreur introduite par l'étape courante doit être corrigée.

Une erreur ne doit pas être déclarée « hors périmètre » uniquement parce qu'elle apparaît dans un autre fichier.

Si une limitation réellement indépendante subsiste, elle doit être documentée clairement.

---

# 23. Docker et changements d'arborescence

L'organisation actuelle est :

```text
pyproject.toml
uv.lock

src/backend/
src/frontend/
```

Toute modification Docker doit vérifier explicitement :

* contexte de build ;
* chemin du Dockerfile ;
* commandes `COPY` ;
* volumes ;
* working directory ;
* accès à `pyproject.toml` ;
* accès à `uv.lock` ;
* chemin du backend ;
* chemin du frontend.

Ne pas réintroduire d'anciens chemins tels que :

```text
backend/
frontend/
backend/pyproject.toml
backend/uv.lock
```

---

# 24. Commandes de diagnostic utiles

## Version Python

```bash
python --version
```

ou :

```bash
uv run python --version
```

## Version uv

```bash
uv --version
```

## Vérification du lockfile

```bash
uv lock --check
```

## État Docker

```bash
docker compose ps
```

## État Alembic

```bash
uv run alembic current
```

## Tests backend

```bash
uv run pytest src/backend/tests -q
```

---

# 25. Règles importantes

* exécuter les commandes uv depuis la racine ;
* ne pas modifier `uv.lock` manuellement ;
* ne pas utiliser un workflow Python parallèle basé sur `requirements.txt` ;
* ne pas lancer Ruff ou ty volontairement sur `src/backend/tests/` ;
* utiliser Alembic pour faire évoluer le schéma ;
* ne pas utiliser les sites d'emploi réels dans les tests automatisés ;
* ne pas versionner `.env` ;
* ne pas mettre de secrets dans Git ;
* ne pas ajouter de dépendance sans besoin réel ;
* ne pas commencer une nouvelle étape de roadmap automatiquement.

---

# 26. Résumé des commandes principales

## Installation

```bash
uv sync
```

## Backend

```bash
uv run uvicorn app.main:app --app-dir src/backend --reload --host 0.0.0.0 --port 8000
```

## Frontend

```bash
cd src/frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## Migrations

```bash
uv run alembic upgrade head
```

## Quality gate

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

## Docker

```bash
docker compose up --build
```

## Arrêt Docker

```bash
docker compose down
```
