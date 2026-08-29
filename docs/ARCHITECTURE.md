# Architecture du projet — Étape 0

Statut : validé pour le cadrage initial du MVP.

Ce document transforme la spécification produit en architecture concrète pour le monolithe modulaire du projet. Il remplace les hypothèses implicites par des décisions d’architecture explicites et reste conforme aux contraintes définies dans le dépôt, en particulier dans AGENTS.md et dans la spécification produit.

## 1. Principe directeur

Le projet est conçu comme un monolithe modulaire, pas comme une architecture distribuée.

Les raisons de ce choix pour le MVP :

- simplicité de développement local ;
- faible coût d’exploitation ;
- tests plus faciles ;
- évolution progressive sans couplage excessif ;
- séparation claire de responsabilités sans microservices prématurés.

Le cœur du système repose sur :

- un backend Python / FastAPI ;
- une base PostgreSQL comme source de vérité ;
- un frontend React + TypeScript avec Vite ;
- une séparation par domaines métier cohérents ;
- des interfaces claires entre collecte, normalisation, déduplication, matching et API.

---

## 2. Périmètre exact du MVP

Le MVP couvre uniquement le noyau de décision et de suivi d’offres accessibles à un usage personnel.

### Inclus dans le MVP

- collecte d’offres depuis plusieurs sources autorisées ;
- conservation des données brutes sous forme de snapshots ;
- normalisation d’annonces dans un modèle canonique commun ;
- déduplication conservative et traçable ;
- profil utilisateur avec préférences structurées ;
- matching déterministe basé sur des règles explicites ;
- API REST pour lire et modifier les entités principales ;
- interface web simple pour lister les offres et consulter le score ;
- suivi des candidatures et interactions de base ;
- tests unitaires et d’intégration sur les composants métier critiques ;
- environnement local Docker avec PostgreSQL et application web.

### Exclus du MVP

- microservices ;
- workers séparés / queue de tâches ;
- Redis, Celery ou autre orchestrateur de jobs ;
- recherche sémantique vectorielle ;
- IA générative pour l’explication du score ;
- import de CV PDF/DOCX ;
- apprentissage automatique adaptatif ;
- intégration à des fournisseurs IA externes en production ;
- alertes push ou email automatisées ;
- scraping furtif ou contournant les protections.

Le MVP doit rester capable de démontrer la valeur métier principale :

> identifier les offres réellement pertinentes pour le profil utilisateur, avec un score explicable et une traçabilité claire.

---

## 3. Architecture générale cible

```text
Client web / dashboard
        │
        ▼
React + TypeScript + Vite
        │
        ├── pages / routes / features
        │
        ▼
FastAPI REST API
        │
        ├── routes / dependencies / schemas
        │
        ▼
Application services
        ├── profile
        ├── jobs
        ├── applications
        ├── interactions
        ├── collection
        ├── normalization
        ├── deduplication
        ├── matching
        ├── enrichment
        └── ai (abstraction future)
        │
        ▼
PostgreSQL
        ├── canonical job data
        ├── source records / occurrences
        ├── user profile / preferences
        ├── interactions / applications
        └── collection run metadata
```

L’API est la seule façade externe. Les composants métier ne doivent pas dépendre directement du frontend.

---

## 4. Structure cible du repository

La structure cible du dépôt doit suivre un découpage simple et lisible, sans sur-ingénierie.

```text
job_manager/
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── .env.example
├── .gitignore
├── docs/
│   ├── PROJET_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   ├── DEVELOPMENT.md
│   └── adr/
│       ├── ADR-001-modular-monolith.md
│       ├── ADR-002-python-tooling.md
│       └── ADR-003-deterministic-matching.md
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── deps/
│   │   │   └── routes/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   └── migrations/
│   │   ├── jobs/
│   │   │   ├── domain/
│   │   │   ├── schemas/
│   │   │   └── services/
│   │   ├── profile/
│   │   ├── applications/
│   │   ├── interactions/
│   │   ├── collection/
│   │   │   ├── sources/
│   │   │   ├── parsers/
│   │   │   └── services/
│   │   ├── normalization/
│   │   ├── deduplication/
│   │   ├── matching/
│   │   ├── enrichment/
│   │   └── ai/
│   └── tests/
│       ├── unit/
│       ├── integration/
│       ├── fixtures/
│       └── conftest.py
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── src/
│       ├── api/
│       ├── components/
│       ├── features/
│       ├── hooks/
│       ├── layouts/
│       ├── pages/
│       ├── routes/
│       ├── types/
│       ├── utils/
│       └── main.tsx
└── .github/
    └── workflows/
```

L’architecture cible conserve la simplicité : un seul backend, un seul database, un seul frontend, sans couche de workers distincte pour le MVP.

---

## 5. Domaines backend principaux

### 5.1 Jobs

Responsable de la gestion des offres canonisées, de leurs états, et des éventuels points d’entrée d’accès API.

Sous-domaines :

- domaine JobOffer ;
- schemas Pydantic ;
- services de lecture / listing / filtres ;
- repository d’offres.

### 5.2 Collection

Responsable de la récupération des données externes depuis des sources autorisées.

Sous-domaines :

- source adapters ;
- fetchers HTTP ;
- parseurs HTML/XML/JSON ;
- services de collecte avec gestion d’erreurs, timeout et retry ;
- stockage des RawJobSnapshot.

### 5.3 Normalization

Responsable du passage d’un RawJob vers un JobOfferCandidate cohérent.

Rôle :

- validation minimale ;
- parse / normalisation de titres, localisations, contrat, dates, technologies ;
- conservation des valeurs brutes et normalisées lorsque nécessaire.

### 5.4 Deduplication

Responsable de la détection de doublons sans destruction des données sources.

Rôle :

- identifiants forts ;
- fingerprint ;
- similarité floue ;
- attachement à une offre canonique ;
- stockage de preuves de décision.

### 5.5 Matching

Responsable de la comparaison entre offre et profil utilisateur.

Rôle :

- règles déterministes ;
- if/else explicites ;
- scores par composante ;
- critères éliminatoires ;
- versioning du moteur ;
- explication lisible.

### 5.6 Profile

Responsable du profil utilisateur et des préférences.

Rôle :

- champs structurés ;
- niveaux de préférence ;
- critères obligatoires ou éliminatoires ;
- édition via API et interface.

### 5.7 Applications / Interactions

Responsable du suivi des candidatures et des actions utilisateur.

Rôle :

- candidatures ;
- interactions telles que favorite / reject / archive / apply ;
- historique exploitable ultérieurement pour apprentissage.

### 5.8 Core / infrastructure

Responsable des éléments transverses :

- configuration ;
- logging ;
- exceptions métier ;
- session DB ;
- migrations ;
- supervision des erreurs.

---

## 6. Modèle de données initial

Le modèle initial doit rester lisible et éviter les tables géantes. Il doit séparer les concepts métier sans sur-ingénierie.

### 6.1 JobSource

- id
- name
- base_url
- collection_method
- enabled
- rate_limit
- last_checked_at
- metadata

### 6.2 RawJobSnapshot

- id
- source_id
- external_job_id
- source_url
- payload
- raw_html
- content_hash
- collected_at

### 6.3 JobOffer

- id
- title
- company_name
- company_description
- description
- normalized_description
- job_type
- contract_type
- location_text
- city
- region
- country
- remote_type
- salary_min
- salary_max
- salary_currency
- salary_period
- duration
- experience_level
- education_level
- industry
- job_category
- publication_date
- expiration_date
- first_seen_at
- last_seen_at
- status
- created_at
- updated_at

### 6.4 JobOccurrence / source record

Représente une occurrence source liée à une offre canonique.

Attributs clés :

- id
- job_offer_id
- source_id
- external_job_id
- source_url
- collected_at
- raw_snapshot_id
- is_primary
- status

### 6.5 UserProfile

- id
- education
- degrees
- experiences
- skills
- technologies
- languages
- preferred_locations
- mobility_radius
- remote_preference
- contract_types
- job_types
- industries
- preferred_roles
- excluded_roles
- salary_expectations
- availability_date
- internship_duration
- preferred_companies
- excluded_companies

### 6.6 UserPreference

- id
- profile_id
- criterion_name
- level
- value
- reason

Valeurs de niveau : REQUIRED / VERY_IMPORTANT / IMPORTANT / BONUS / AVOID / EXCLUDED.

### 6.7 Interaction

- id
- job_offer_id
- profile_id
- interaction_type
- created_at
- metadata

### 6.8 MatchResult

- id
- job_offer_id
- profile_id
- score
- eligible
- scoring_version
- component_scores
- matched_items
- missing_items
- blocking_reasons
- explanation_data
- computed_at

### 6.9 Application

- id
- job_offer_id
- company
- position
- status
- application_date
- follow_up_date
- cv_reference
- cover_letter_reference
- notes
- contacts
- next_action
- created_at
- updated_at

Les compétences, technologies, langues et autres données structurées sont d’abord stockées avec une modélisation simple et explicite, puis peu à peu affinées selon les besoins métier.

---

## 7. Pipeline de collecte

Le pipeline doit être explicite et ordonné.

```text
Source externe
   │
   ▼
Collecteur / fetcher
   │
   ▼
RawJobSnapshot
   │
   ▼
Parsing
   │
   ▼
Normalisation
   │
   ▼
JobOfferCandidate
   │
   ▼
Déduplication
   │
   ▼
Enrichissement
   │
   ▼
Matching
   │
   ▼
API / dashboard
```

### Règles de conception

- chaque source implémente une interface commune ;
- le collecteur ne fait pas la logique métier globale ;
- l’erreur d’une source ne casse pas les autres sources ;
- les données brutes doivent rester disponibles pour retraitement ;
- la collecte doit être déclenchable manuellement au MVP ;
- chaque run doit avoir un identifiant de corrélation et des statistiques de résultat.

### À retenir pour les sources

Avant d’ajouter un collecteur réel :

1. vérifier s’il existe une API officielle ;
2. rechercher un feed RSS/XML structuré ;
3. vérifier le respect de robots.txt, terms, rate limits et protections ;
4. documenter la méthode retenue ;
5. limiter la fréquence à un rythme raisonnable.

---

## 8. Stratégie de normalisation

La normalisation n’est pas une simple transformation d’une chaîne en une autre. Elle doit conserver la provenance des informations pour rester explicable.

### Règles

- garder les valeurs brutes et les valeurs normalisées quand cela aide à la compréhension ;
- normaliser les champs structurels de base : titres, entreprises, localisations, contrat, salaire, technologies, dates ;
- ne pas supposer qu’un champ absent est un mismatch ;
- produire des données standardisées en vue du matching et des filtres.

### Exemple de contrat de normalisation

```text
RawJob
  -> validate
  -> parse
  -> normalize
  -> JobOfferCandidate
```

Les composants de normalisation doivent être testés de manière indépendante, avec des fixtures de cas réels et dégradés.

---

## 9. Déduplication

La déduplication doit être progressive, explicable et conservatrice.

### Niveaux

1. Identifiants forts
   - source + external_job_id ;
   - URL canonique ;
   - content hash exact.

2. Fingerprint déterministe
   - company + title + location + contract.

3. Similarité floue
   - titre proche,
   - description proche,
   - périodicité / dates cohérentes.

4. Similarité sémantique (future)
   - uniquement dans une couche plus avancée, après stabilisation de la base.

### Règle clé

Les doublons confirmés sont rattachés à une offre canonique ; ils ne sont pas supprimés brutalement. L’historique de la provenance est conservé.

---

## 10. Matching déterministe

Le moteur de matching V1 est entièrement déterministe.

### Objectif

Calculer un score explicable à partir de plusieurs composantes, par exemple :

- skills ;
- technologies ;
- location ;
- contract ;
- education ;
- experience ;
- languages ;
- industry ;
- remote ;
- salary ;
- duration ;
- role.

### Calcul

```text
final_score = Σ(component_score × component_weight)
```

### Règle de gestion de l’incertitude

- MATCH : critère vérifié ou compatible ;
- MISMATCH : critère explicitement contradictoire ;
- UNKNOWN : information absente ou non fournie.

L’absence d’information doit être traitée comme inconnue, pas comme incompatibilité.

### Critères éliminatoires

Les critères éliminatoires sont distincts du score :

- contrat incompatible ;
- localisation non compatible ;
- durée insuffisante ;
- diplôme requis non satisfait ;
- compétence obligatoire absente ;
- langue ou type de poste non compatible.

Ils doivent être configurables par profile et par version du moteur.

---

## 11. Responsabilités backend / frontend

### Backend

- exposer les endpoints REST ;
- gérer l’intégrité des données ;
- orchestrer les services métier ;
- gérer les migrations, session DB et config ;
- faire les calculs métier ;
- rendre les données en structure cohérente pour le frontend.

### Frontend

- afficher les données de manière claire ;
- permettre la recherche, les filtres et les interactions ;
- présenter les scores et leurs explications ;
- gérer l’état local minimal et les erreurs API ;
- laisser le backend être la source de vérité.

### Séparation des responsabilités

Le frontend ne doit pas contenir la logique de scoring ou de déduplication. Ces règles se trouvent côté backend.

---

## 12. Stratégie de tests

Le projet suivra un modèle backend orienté métier avec des tests unitaires et d’intégration.

### Tests unitaires

À couvrir absolument :

- normalisation ;
- parsing ;
- déduplication ;
- matching ;
- critères éliminatoires ;
- calcul des scores ;
- gestion des UNKNOWN ;
- configuration.

### Tests d’intégration

- API FastAPI ;
- repositories PostgreSQL ;
- migrations ;
- pipeline complet de collecte ;
- canaux de données entre modules.

### Fixtures de sources

Pour chaque collecteur réel, la suite de tests utilisera :

- HTML ou JSON représentant des payloads réels anonymisés ;
- expectations de parsing ;
- cas d’erreurs ;
- cas de changements de structure.

Les tests ne doivent pas dépendre de sites web externes en production.

---

## 13. Stratégie Docker

Le niveau MVP n’introduit qu’un environnement local simple.

```text
docker-compose.yml
├── postgres
├── backend
└── frontend
```

### Objectifs

- rendre le démarrage local simple ;
- garantir une base PostgreSQL reproductible ;
- aligner les dépendances avec uv / uv.lock ;
- éviter les composants non nécessaires au MVP.

Il ne faut pas ajouter immédiatement :

- worker ;
- Redis ;
- celery ;
- services de queue.

---

## 14. Rôle de uv, Ruff et ty

### uv

- gestionnaire principal du projet Python ;
- contrôle des dépendances, de l’environnement virtuel et du lockfile ;
- commande de référence pour le backend.

### Ruff

- linting et formatage du code Python ;
- validation minimale attendue du projet :

```bash
uv run ruff check .
uv run ruff format --check .
```

### ty

- vérification statique des types ;
- impose un typage rigoureux sur les modules métier critiques ;
- évite les `Any` inutiles et les erreurs de contrat dans les services et modèles.

Le quality gate du backend est :

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

---

## 15. Principaux risques et points de vigilance

### Risque 1 — trop de complexité dès le départ

La valeur principale du projet n’est pas la sophistication technique, mais la qualité du tri et de l’explication. Il faut éviter les couches inutiles avant le besoin réel.

### Risque 2 — collecte bloquée par la qualité des sources

Les sources peuvent changer de structure, appliquer des restrictions ou devenir inaccessibles. Il faut donc traiter chaque source comme un composant isolé et testable.

### Risque 3 — perte d’information au moment de la normalisation

Une normalisation trop agressive peut détruire le sens d’une annonce. Les champs originaux restent donc disponibles pour un retraitement ou une analyse avancée.

### Risque 4 — faux positifs de déduplication

Le système doit être conservateur. Un doublon confirmé doit être rattaché à une offre canonique, pas supprimé sans preuve.

### Risque 5 — score opaques ou non explicables

Le moteur de matching doit être lisible et reproductible. Les scores doivent être perçus comme des décisions compréhensibles, et non comme des boîtes noires.

### Risque 6 — données personnelles et confidentialité

Le CV, les préférences, les candidatures et les interactions sont sensibles. Les intégrations IA doivent rester minimales, configurables et éventuellement locales.

---

## 16. Décision d’architecture retenue

Pour l’étape 0, la décision est la suivante :

- un monolithe modulaire sur Python / FastAPI ;
- PostgreSQL comme source de vérité ;
- React + TypeScript + Vite pour le frontend ;
- séparation claire entre collecte, normalisation, déduplication, matching et API ;
- moteur de matching V1 entièrement déterministe ;
- qualité logicielle imposée par uv / Ruff / ty ;
- Docker local sans workers ni redis pour le MVP ;
- documentation d’architecture et ADRs comme éléments de référence pour les étapes suivantes.

Cette architecture correspond au bon niveau d’abstraction pour commencer sans sur-contraindre le projet.
