# Roadmap du projet

Statut actuel : Étape 4 — Fondation FastAPI mise en place : application factory, routeur versionné, endpoints de santé, gestion centralisée des erreurs, CORS, dépendances FastAPI, tests API et documentation OpenAPI. Le démarrage du backend HTTP est validé localement.

La roadmap suit la logique de développement incrémental définie dans AGENTS.md et la spécification produit. Le projet ne doit pas avancer vers l'étape suivante sans validation de l'architecture de l'étape courante.

---

## Étape 0 — Architecture

Objectif : transformer la spécification produit en architecture cohérente et exécutable pour un MVP personnel.

Livrables attendus :

- architecture modulaire du monolithe ;
- périmètre exact du MVP ;
- structure cible du repository ;
- domaines backend et responsabilités ;
- modèle de données initial ;
- pipeline de collecte et de normalisation ;
- stratégie de déduplication et de matching ;
- stratégie de tests et Docker ;
- ADRs et décisions structurantes.

### État

Validé et documenté dans [docs/ARCHITECTURE.md](ARCHITECTURE.md) et les ADRs associés.

---

## Étape 1 — Bootstrap du repository

Objectif : mettre en place le squelette technique initial du projet.

### Terminé dans ce lot

- backend Python avec FastAPI ;
- frontend React + TypeScript + Vite ;
- configuration uv et lockfile ;
- Ruff, ty et pytest installés et validés ;
- configuration TypeScript stricte ;
- fichier de base Git ignore ;
- exemple de variables d'environnement ;
- documentation de démarrage minimale.

### État

Terminé et validé.

---

## Étape 2 — Infrastructure locale

Objectif : permettre un démarrage local reproductible avec PostgreSQL et Docker Compose, sans implémenter de logique métier.

### Inclu dans cette étape

- service PostgreSQL avec volume persistant ;
- service backend Docker ;
- service frontend Docker ;
- configuration d'environnement centralisée ;
- variables Docker/PostgreSQL ;
- health checks basiques ;
- documentation de démarrage local ;
- cohérence backend / Docker / uv.

### Non inclus dans cette étape

- modèles SQLAlchemy métier ;
- migrations de persistance ;
- JobOffer, UserProfile, collecteur ou matching ;
- fonction de business logic ;
- toute étape d'implémentation métier.

### État

Configuration mise en place dans le dépôt. Le runtime Docker réel n'a pas pu être validé dans cet environnement car Docker est absent. La synthèse YAML et les vérifications Python effectuées sont correctes, mais le lancement de `docker compose up` reste à exécuter sur une machine avec Docker installé.

---

## Étape 3 — Modèle métier et persistance

### Objectif

Implémenter les premiers modèles de données, repositories et migrations initiales.

### Inclus dans cette étape

- modèles SQLAlchemy : JobSource, RawJobSnapshot, JobOffer, JobSourceOccurrence ;
- configuration centralisée de la base de données ;
- session SQLAlchemy et engine ;
- Alembic connecté à la metadata SQLAlchemy ;
- migration initiale du schéma ;
- tests de persistance ;
- intégration avec le backend FastAPI.

### État

Première couche de persistance mise en place dans le backend : modèles SQLAlchemy responsables du stockage des sources, snapshots bruts, offres canonisées et occurrences, avec connexion Alembic vers la metadata partagée. La migration initiale est créée dans le dépôt et les tests de modèle passent localement. La validation complète avec PostgreSQL réel reste dépendante de Docker ou d'un service Postgres disponible.

---

## Étape 4 — Fondation API FastAPI

### Objectif

Mettre en place une base FastAPI propre, robuste et extensible qui servira de fondation aux futurs endpoints métier.

### Inclus dans cette étape

- application FastAPI avec factory (`create_app()`) ;
- structure des routes avec versionnage `/api/v1` ;
- dépendances FastAPI pour l'injection de sessions SQLAlchemy (`get_db()`) ;
- endpoints de santé (liveness `/health` et readiness `/health/ready`) ;
- gestion centralisée des erreurs et des exceptions métier ;
- hiérarchie d'exceptions structurées (`ApplicationError`, `DatabaseError`, `ServiceUnavailableError`) ;
- format cohérent des réponses d'erreur API ;
- validation Pydantic sur les schémas API ;
- CORS configuré pour le développement local (origins `localhost:5173` et `localhost:3000`) ;
- documentation OpenAPI, Swagger UI et ReDoc ;
- tests API fondamentaux pour les endpoints techniques ;
- intégration avec la couche SQLAlchemy créée à l'Étape 3.

### Non inclus dans cette étape

- routes métier complètes (CRUD JobOffer, Profile, etc.) ;
- authentification ou autorisation ;
- logique métier de collecte, normalisation ou matching ;
- profil utilisateur ;
- endpoint de recherche ou filtrage métier ;
- fonctionnalités frontend.

### État

Fondation API terminée et validée : application factory créée, routeur versionné préparé, endpoints de santé implémentés, gestion centralisée des erreurs en place, tests API passants, documentation OpenAPI disponible. Le backend peut démarrer localement avec uvicorn et servir les endpoints de santé et la documentation.

---

## Étape 5 — Profil utilisateur et préférences

### Objectif

Implémenter la première entité métier : le profil utilisateur avec ses préférences structurées.

### Sous-étapes

- modèle UserProfile et UserPreference ;
- migration initiale UserProfile ;
- repository UserProfile ;
- endpoints CRUD `/api/v1/profile` ;
- tests de profil utilisateur ;
- validation des préférences.

---

## Étape 6 — Collecte et normalisation

### Objectif

Construire le canal d'acquisition des données sources.

### Sous-étapes

- interface commune des sources ;
- collecteur de test / fixtures ;
- parsing et validation ;
- normalisation structurée ;
- stockage des snapshots bruts ;
- gestion des erreurs et des taux de collecte.

---

## Étape 7 — Déduplication et matching déterministe

### Objectif

Faire fonctionner les mécanismes de tri et de recommandation.

### Sous-étapes

- fingerprint et déduplication progressive ;
- matching V1 par composantes ;
- critères éliminatoires ;
- versioning du moteur de scoring ;
- explication des recommandations.

---

## Étape 8 — Frontend MVP

### Objectif

Mettre en place l'interface utilisateur principale.

### Sous-étapes

- écran liste des offres ;
- filtres et recherche ;
- détails d'une offre ;
- profil utilisateur ;
- favoris / rejet / archive ;
- suivi des candidatures.

---

## Étape 9 — Évolution du système

### Objectif

Introduire des fonctionnalités ciblées seulement après la stabilité du MVP.

### Axes possibles

- enrichissement NLP local ;
- recherche sémantique PostgreSQL + pgvector ;
- revue du scoring ;
- apprentissage sur interactions ;
- suggestions de préférences ;
- imports de CV ;
- alertes et automatisation si nécessaire.

---

## Points de contrôle de projet

Avant chaque nouvelle étape, vérifier :

- cohérence avec l'architecture décidée ;
- documentation en cours de validité ;
- présence de tests adaptés ;
- absence de sur-ingénierie ;
- respect du périmètre de la step courante.
