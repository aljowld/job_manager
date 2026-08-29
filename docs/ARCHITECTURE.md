# Architecture du projet

**Statut : architecture validée pour le MVP et mise à jour avec l'organisation actuelle du repository.**

Ce document transforme la spécification produit en architecture concrète pour le monolithe modulaire du projet.

Il décrit les décisions architecturales réellement retenues.

Documents de référence :

* `.github/copilot-instructions.md` définit les règles permanentes de travail pour GitHub Copilot ;
* `docs/PROJECT_SPEC.md` définit les besoins et contraintes produit ;
* `docs/ROADMAP.md` définit l'ordre et le périmètre des étapes de développement ;
* `docs/DEVELOPMENT.md` décrit les commandes et workflows de développement.

En cas de conflit entre une ancienne hypothèse de la spécification et une décision déjà validée et documentée ici, cette architecture représente l'état architectural actuellement retenu.

---

# 1. Principe directeur

Le projet est conçu comme un **monolithe modulaire**, et non comme une architecture distribuée.

Les raisons de ce choix pour le MVP sont :

* simplicité de développement local ;
* faible coût d'exploitation ;
* tests plus faciles ;
* déploiement simple ;
* évolution progressive ;
* séparation claire des responsabilités ;
* absence de besoin réel en microservices à ce stade.

Le cœur du système repose sur :

* un backend Python / FastAPI ;
* PostgreSQL comme source de vérité ;
* SQLAlchemy 2 pour la persistence ;
* Alembic pour les migrations ;
* Pydantic v2 pour les contrats et validations ;
* un frontend React + TypeScript avec Vite ;
* une séparation par domaines métier ;
* des interfaces claires entre collecte, normalisation, déduplication, matching et API.

Principe général :

```text
simplicité
    ↓
séparation des responsabilités
    ↓
testabilité
    ↓
évolution progressive
```

La complexité ne doit être introduite qu'en réponse à un besoin réel et identifié.

---

# 2. Périmètre exact du MVP

Le MVP couvre le noyau de collecte, décision, consultation et suivi des offres pour un usage personnel.

## Inclus dans le MVP

* profil utilisateur avec préférences structurées ;
* collecte d'offres depuis des sources autorisées ;
* conservation des données brutes sous forme de snapshots ;
* normalisation des annonces ;
* stockage dans un modèle canonique ;
* déduplication conservatrice et traçable ;
* matching déterministe basé sur des règles explicites ;
* explication des scores ;
* API REST ;
* consultation et filtrage des offres ;
* interface web ;
* favoris, rejets et archivage ;
* suivi des candidatures ;
* tests unitaires et d'intégration ;
* environnement local Docker avec PostgreSQL.

## Exclus du MVP

* microservices ;
* workers distribués ;
* Redis ;
* Celery ;
* Kafka ou autre message broker ;
* Elasticsearch ;
* base vectorielle séparée ;
* recherche sémantique ;
* embeddings ;
* IA générative pour le scoring ;
* import automatique de CV ;
* apprentissage automatique adaptatif ;
* alertes automatiques ;
* infrastructure cloud complexe ;
* Kubernetes ;
* scraping contournant des protections techniques.

Le MVP doit démontrer la valeur principale du produit :

> Identifier les offres réellement pertinentes pour le profil utilisateur, expliquer pourquoi elles sont pertinentes et permettre de suivre efficacement leur traitement.

---

# 3. Architecture générale

```text
┌────────────────────────────────────────────┐
│                 Frontend                   │
│          React + TypeScript + Vite         │
└─────────────────────┬──────────────────────┘
                      │
                   REST API
                      │
                      ▼
┌────────────────────────────────────────────┐
│                 FastAPI                    │
│                                            │
│  routes / dependencies / schemas / errors │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────┐
│            Application Services            │
│                                            │
│  profile                                   │
│  jobs                                      │
│  applications                              │
│  interactions                              │
│  collection                                │
│  normalization                             │
│  deduplication                             │
│  matching                                  │
│  enrichment (future)                       │
│  ai (future)                               │
└─────────────────────┬──────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────┐
│                 Persistence                │
│                                            │
│       SQLAlchemy 2 + PostgreSQL            │
│                                            │
│  canonical jobs                            │
│  source occurrences                        │
│  raw snapshots                             │
│  profiles/preferences                      │
│  interactions                              │
│  applications                              │
│  match results                             │
└────────────────────────────────────────────┘
```

Le frontend ne constitue jamais la source de vérité métier.

L'API est la façade applicative principale.

La logique métier doit rester indépendante du frontend et, autant que possible, des détails propres à FastAPI.

---

# 4. Organisation actuelle du repository

Le repository utilise actuellement l'organisation suivante :

```text
job_manager/
├── pyproject.toml
├── uv.lock
├── alembic.ini
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
│
├── src/
│   ├── backend/
│   │   ├── alembic/
│   │   │   ├── env.py
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   │
│   │   ├── app/
│   │   │   ├── factory.py
│   │   │   ├── main.py
│   │   │   │
│   │   │   ├── api/
│   │   │   │   ├── dependencies.py
│   │   │   │   ├── router.py
│   │   │   │   └── routes/
│   │   │   │       ├── health.py
│   │   │   │       └── profile.py
│   │   │   │
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   └── exceptions.py
│   │   │   │
│   │   │   ├── db/
│   │   │   │   ├── base.py
│   │   │   │   ├── models.py
│   │   │   │   └── session.py
│   │   │   │
│   │   │   └── schemas/
│   │   │       └── profile.py
│   │   │
│   │   └── tests/
│   │       ├── test_api_setup.py
│   │       ├── test_error_handling.py
│   │       ├── test_health.py
│   │       ├── test_persistence_setup.py
│   │       └── test_profile_api.py
│   │
│   └── frontend/
│       ├── index.html
│       ├── package.json
│       ├── package-lock.json
│       ├── tsconfig.json
│       ├── tsconfig.app.json
│       ├── tsconfig.node.json
│       ├── vite.config.ts
│       └── src/
│           ├── main.tsx
│           └── styles.css
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

Cette arborescence représente une organisation de repository, et non une architecture microservices.

`src/backend/` et `src/frontend/` restent deux composants d'une même application.

---

# 5. Racine du projet Python

Le projet Python est maintenant configuré depuis la **racine du repository**.

Les fichiers suivants sont à la racine :

```text
pyproject.toml
uv.lock
```

La racine du repository constitue donc la racine de travail pour :

* uv ;
* Ruff ;
* ty ;
* configuration pytest.

Le code applicatif Python est situé dans :

```text
src/backend/app/
```

Les tests backend sont situés dans :

```text
src/backend/tests/
```

Cette organisation doit être prise en compte par :

* Docker ;
* Alembic ;
* scripts ;
* documentation ;
* commandes de développement ;
* outils de qualité.

---

# 6. Domaines backend

## 6.1 Profile

Responsable du profil utilisateur et des préférences.

Responsabilités :

* données structurées du profil ;
* compétences ;
* technologies ;
* langues ;
* localisation ;
* mobilité ;
* préférences de contrat ;
* préférences de poste ;
* niveaux de préférence ;
* critères obligatoires ;
* exclusions ;
* persistence ;
* validation ;
* API du profil.

Le profil constitue la source de vérité du futur moteur de matching.

---

## 6.2 Jobs

Responsable des offres canonisées.

Responsabilités :

* domaine `JobOffer` ;
* schémas Pydantic ;
* consultation ;
* listing ;
* pagination ;
* filtres ;
* tri ;
* détail d'une offre ;
* relations avec les occurrences sources.

Le domaine `Jobs` ne réalise pas directement la collecte.

---

## 6.3 Collection

Responsable de l'acquisition des données externes.

Responsabilités :

* adapters de sources ;
* appels HTTP ;
* parsing source ;
* gestion des timeouts ;
* retries raisonnés ;
* rate limiting ;
* gestion des erreurs ;
* création de données brutes ;
* alimentation des `RawJobSnapshot`.

Un collecteur ne doit pas contenir toute la logique de normalisation, déduplication et matching.

---

## 6.4 Normalization

Responsable de la transformation des données collectées en représentation cohérente.

Responsabilités :

* validation minimale ;
* normalisation des titres ;
* entreprises ;
* localisations ;
* contrats ;
* remote ;
* dates ;
* salaires ;
* technologies ;
* autres données structurées utiles.

La normalisation doit conserver les données brutes lorsque cela améliore la traçabilité.

---

## 6.5 Deduplication

Responsable de déterminer si plusieurs occurrences représentent probablement la même offre.

Responsabilités :

* identifiants forts ;
* URL canonique ;
* hashes ;
* fingerprints ;
* similarité floue lorsque nécessaire ;
* rattachement à une offre canonique ;
* préservation de la provenance.

La déduplication est conservatrice et non destructive.

---

## 6.6 Matching

Responsable de déterminer si une offre est pertinente pour le profil utilisateur.

Responsabilités :

* règles déterministes ;
* scores par composante ;
* pondérations ;
* critères éliminatoires ;
* gestion de l'incertitude ;
* version du scoring ;
* génération d'explications basées sur les calculs réels.

Le matching ne doit pas être confondu avec la déduplication.

---

## 6.7 Applications

Responsable du suivi des candidatures.

Responsabilités futures du MVP :

* création d'une candidature ;
* statut ;
* dates ;
* relances ;
* notes ;
* contacts ;
* prochaine action.

---

## 6.8 Interactions

Responsable des actions utilisateur liées aux offres.

Types initiaux prévus :

* view ;
* favorite ;
* reject ;
* archive ;
* apply.

Ces données pourront être utilisées plus tard pour suggérer des ajustements de préférences, mais pas pour modifier automatiquement le profil.

---

## 6.9 Enrichment

Module prévu pour les enrichissements avancés.

Il reste hors du noyau MVP initial tant que les besoins déterministes suffisent.

---

## 6.10 AI

Module futur.

Il devra permettre, lorsque la roadmap l'autorise :

* embeddings ;
* extraction assistée ;
* LLM ;
* fournisseurs externes ou locaux.

Le domaine métier ne doit pas devenir dépendant d'un fournisseur IA spécifique.

---

# 7. Infrastructure backend transverse

Les responsabilités transversales comprennent :

* configuration ;
* logging ;
* exceptions ;
* persistence ;
* sessions SQLAlchemy ;
* migrations Alembic ;
* injection de dépendances FastAPI ;
* erreurs API ;
* OpenAPI ;
* health checks.

Ces éléments doivent être partagés et réutilisés.

Il ne faut pas créer plusieurs systèmes concurrents de :

* configuration ;
* sessions SQLAlchemy ;
* gestion des erreurs ;
* logging.

---

# 8. Modèle de données

Le modèle de données doit rester explicite et éviter les tables gigantesques ou les documents JSON contenant tout le domaine.

## 8.1 JobSource

Représente une source d'offres.

Attributs conceptuels :

```text
id
name
base_url
collection_method
enabled
rate_limit
last_checked_at
metadata
```

---

## 8.2 RawJobSnapshot

Représente une copie brute des données collectées.

Attributs conceptuels :

```text
id
source_id
external_job_id
source_url
payload
raw_html
content_hash
collected_at
```

Objectif principal :

> permettre de retraiter ultérieurement les données sans devoir systématiquement recontacter la source.

---

## 8.3 JobOffer

Représente une offre canonique.

Attributs conceptuels :

```text
id

title
company_name
company_description

description
normalized_description

job_type
contract_type

location_text
city
region
country
remote_type

salary_min
salary_max
salary_currency
salary_period

duration

experience_level
education_level

industry
job_category

publication_date
expiration_date

first_seen_at
last_seen_at

status

created_at
updated_at
```

Ce modèle pourra évoluer via migrations à mesure que les besoins fonctionnels sont implémentés.

---

## 8.4 JobSourceOccurrence

Représente une occurrence d'une offre provenant d'une source.

```text
id
job_offer_id
source_id
external_job_id
source_url
collected_at
raw_snapshot_id
is_primary
status
```

Une même `JobOffer` peut avoir plusieurs `JobSourceOccurrence`.

C'est la base de la stratégie de déduplication non destructive.

---

## 8.5 UserProfile

Représente le profil personnel utilisé pour la recherche et le matching.

Il peut contenir notamment :

```text
id

education
degrees
experiences

skills
technologies
languages

preferred_locations
mobility_radius
remote_preference

contract_types
job_types
industries

preferred_roles
excluded_roles

salary_expectations

availability_date
internship_duration

preferred_companies
excluded_companies
```

La modélisation réellement implémentée peut utiliser plusieurs tables associées afin de rendre certaines données interrogeables et normalisées.

---

## 8.6 UserPreference

Représente une préférence structurée.

Attributs conceptuels :

```text
id
profile_id
criterion_name
level
value
reason
```

Niveaux :

```text
REQUIRED
VERY_IMPORTANT
IMPORTANT
BONUS
AVOID
EXCLUDED
```

Préférence, exigence et exclusion doivent rester conceptuellement distinguables.

---

## 8.7 Interaction

Prévue pour les interactions utilisateur.

```text
id
job_offer_id
profile_id
interaction_type
created_at
metadata
```

---

## 8.8 MatchResult

Prévu pour conserver ou reproduire le résultat du matching.

```text
id
job_offer_id
profile_id

score
eligible

scoring_version

component_scores
matched_items
missing_items
blocking_reasons
explanation_data

computed_at
```

Le `scoring_version` est important pour la reproductibilité.

---

## 8.9 Application

Prévue pour le suivi des candidatures.

```text
id
job_offer_id

company
position
status

application_date
follow_up_date

cv_reference
cover_letter_reference

notes
contacts
next_action

created_at
updated_at
```

---

# 9. Pipeline de collecte

Le pipeline doit rester explicite.

```text
Source externe
      │
      ▼
Collecteur
      │
      ▼
Raw data
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
JobOffer canonique
      │
      ▼
Matching
      │
      ▼
API
      │
      ▼
Frontend
```

Les étapes doivent être séparées pour pouvoir être :

* testées indépendamment ;
* remplacées ;
* rejouées ;
* observées ;
* corrigées sans toucher aux autres composants.

---

# 10. Architecture des sources

Chaque source doit implémenter un contrat commun ou un protocole équivalent.

Le collecteur doit uniquement gérer ce qui appartient à la source.

Il ne doit pas devenir responsable :

* du matching ;
* des préférences utilisateur ;
* de la déduplication globale ;
* de l'API ;
* de la logique frontend.

Ordre de préférence pour récupérer des offres :

```text
API officielle
      ↓
flux structuré
      ↓
HTTP + parsing
      ↓
crawler spécialisé
      ↓
navigateur automatisé
```

Le navigateur automatisé ne doit être utilisé que lorsque nécessaire et approprié.

---

# 11. Contraintes de collecte

Avant d'ajouter une source réelle :

1. rechercher une API officielle ;
2. rechercher un flux RSS/XML/JSON ;
3. consulter les conditions applicables ;
4. examiner `robots.txt` lorsque pertinent ;
5. vérifier les restrictions ;
6. déterminer une fréquence raisonnable ;
7. documenter la méthode retenue.

Ne jamais contourner :

* CAPTCHA ;
* authentification ;
* paywalls ;
* protections anti-bot ;
* limitations techniques destinées à empêcher l'accès automatisé.

Un échec d'une source ne doit pas faire échouer toutes les autres.

---

# 12. Normalisation

La normalisation doit produire une représentation commune sans perdre inutilement la donnée originale.

Pipeline conceptuel :

```text
RawJob
   ↓
validation
   ↓
parsing
   ↓
normalization
   ↓
JobOfferCandidate
```

Normaliser progressivement :

* titres ;
* entreprises ;
* localisations ;
* villes ;
* pays ;
* contrats ;
* remote/hybrid/on-site ;
* dates ;
* monnaies ;
* salaires ;
* technologies ;
* compétences.

Une valeur absente ne doit pas être transformée artificiellement en incompatibilité.

---

# 13. Déduplication

La déduplication doit être :

* progressive ;
* explicable ;
* conservatrice ;
* non destructive.

## Niveau 1 — Signaux forts

* source + external ID ;
* URL canonique ;
* hash exact.

## Niveau 2 — Fingerprint

Combinaison possible :

```text
company
+
title
+
location
+
contract
```

## Niveau 3 — Similarité floue

Lorsque nécessaire :

* titre ;
* description ;
* localisation ;
* dates.

## Niveau 4 — Similarité sémantique

Post-MVP uniquement si les étapes précédentes ne suffisent pas.

Résultats conceptuels :

```text
NOT_DUPLICATE
POSSIBLE_DUPLICATE
CONFIRMED_DUPLICATE
```

Les occurrences confirmées comme doublons restent conservées et sont reliées à l'offre canonique.

---

# 14. Matching déterministe

Le moteur V1 doit être entièrement déterministe.

Composantes possibles :

* skills ;
* technologies ;
* location ;
* contract ;
* education ;
* experience ;
* languages ;
* industry ;
* remote ;
* salary ;
* duration ;
* role.

Conceptuellement :

```text
final_score =
    somme(component_score × component_weight)
```

Les poids doivent rester configurables.

---

# 15. Gestion de l'incertitude

Le matching doit distinguer :

```text
MATCH
MISMATCH
UNKNOWN
```

Exemple :

```text
Profil :
salaire minimum souhaité = 1500 €

Offre :
salaire non indiqué

Résultat :
UNKNOWN
```

et non :

```text
MISMATCH
```

Une absence d'information ne doit pas être pénalisée comme une contradiction.

---

# 16. Critères éliminatoires

Certains critères sont distincts du score.

Exemples :

* contrat incompatible ;
* localisation réellement incompatible ;
* durée incompatible ;
* disponibilité impossible ;
* diplôme obligatoire absent ;
* compétence explicitement obligatoire absente ;
* langue obligatoire absente ;
* rôle explicitement exclu.

Le moteur doit pouvoir retourner :

```text
eligible = false
```

indépendamment du score pondéré.

---

# 17. Explicabilité du matching

Le moteur ne doit pas seulement retourner :

```text
87 %
```

Il doit pouvoir produire une structure telle que :

```text
Score : 87 %

Points forts
✓ Python
✓ SQL
✓ Machine Learning
✓ localisation compatible

Points faibles
⚠ AWS demandé mais absent du profil

Inconnus
? salaire non indiqué

Critères bloquants
aucun
```

L'explication doit être générée à partir des données réelles ayant participé au calcul.

Un LLM ne doit pas inventer a posteriori une justification sans disposer des éléments du scoring.

---

# 18. Responsabilités backend / frontend

## Backend

Le backend est responsable de :

* persistence ;
* intégrité des données ;
* API ;
* logique métier ;
* normalisation ;
* déduplication ;
* matching ;
* sécurité métier ;
* validation ;
* orchestration.

## Frontend

Le frontend est responsable de :

* affichage ;
* navigation ;
* formulaires ;
* filtres utilisateur ;
* interactions ;
* gestion des états de chargement ;
* présentation des erreurs API.

Le frontend ne doit pas contenir :

* le moteur de matching ;
* les règles de déduplication ;
* les règles métier critiques.

Le backend reste la source de vérité.

---

# 19. Stratégie de tests

Les tests backend vivent dans :

```text
src/backend/tests/
```

pytest est l'outil responsable de leur exécution.

## Tests unitaires

À couvrir progressivement :

* normalisation ;
* parsing ;
* déduplication ;
* matching ;
* critères éliminatoires ;
* scoring ;
* gestion de `UNKNOWN` ;
* validations ;
* services métier.

## Tests d'intégration

À couvrir progressivement :

* API FastAPI ;
* repositories ;
* PostgreSQL ;
* migrations ;
* transactions ;
* pipeline complet ;
* communication entre modules.

## Fixtures de sources

Pour les collecteurs :

* HTML minimal ;
* JSON ;
* XML ;
* payloads enregistrés ;
* cas d'erreur ;
* changements de structure simulés.

Les tests automatisés ne doivent jamais dépendre directement d'un site externe réel pour réussir.

---

# 20. Politique Ruff, ty et pytest

La qualité du code applicatif et celle des tests sont volontairement séparées.

## Code applicatif backend

```text
src/backend/app/
```

est vérifié avec :

* Ruff lint ;
* Ruff format ;
* ty.

## Tests backend

```text
src/backend/tests/
```

sont vérifiés avec :

* pytest.

Les tests sont volontairement exclus de Ruff et ty afin de limiter le coût de maintenance des mocks, fixtures et constructions spécifiques aux tests.

La configuration attendue est conceptuellement :

```toml
[tool.ruff]
extend-exclude = ["src/backend/tests"]

[tool.ty.src]
include = ["src/backend/app"]
exclude = ["src/backend/tests"]

[tool.pytest.ini_options]
testpaths = ["src/backend/tests"]
```

La syntaxe réelle reste celle compatible avec les versions installées et verrouillées du projet.

---

# 21. Toolchain Python

## uv

`uv` est le gestionnaire principal du projet Python.

Il gère :

* environnement Python ;
* dépendances ;
* lockfile ;
* exécution des commandes Python.

Les fichiers de référence sont :

```text
/pyproject.toml
/uv.lock
```

Ils sont situés à la racine du repository.

Les dépendances Python doivent être ajoutées avec `uv`.

`uv.lock` ne doit jamais être modifié manuellement.

---

## Ruff

Ruff assure :

* linting ;
* formatage ;

du code applicatif Python.

Pendant le développement, les corrections automatiques sûres peuvent être appliquées avec :

```bash
uv run ruff check src/backend/app --fix
uv run ruff format src/backend/app
```

`--fix` est la méthode privilégiée pour corriger automatiquement les violations sûres, notamment :

* imports inutilisés ;
* ordre et regroupement des imports ;
* imports dupliqués ;
* autres corrections automatiques sûres proposées par Ruff.

La commande `--fix` ne fait pas partie du quality gate final.

Les validations finales restent non destructives et s’exécutent depuis la racine avec :

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

Les tests backend sont exclus via la configuration du projet.

---

## ty

ty assure la vérification statique des types du code applicatif Python.

Commande :

```bash
uv run ty check
```

Le périmètre principal est :

```text
src/backend/app/
```

---

## pytest

pytest valide le comportement des tests backend.

Commande explicite :

```bash
uv run pytest src/backend/tests
```

Lorsque `testpaths` est correctement configuré, la commande suivante est également valide :

```bash
uv run pytest
```

---

# 22. Quality gate backend

Le quality gate backend est exécuté depuis la racine du repository :

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

Interprétation :

```text
src/backend/app/     Ruff + format + ty
src/backend/tests/   pytest
```

Une étape ne doit pas être déclarée valide si elle introduit une erreur dans ces contrôles.

Les problèmes réellement préexistants et indépendants doivent être :

* identifiés ;
* documentés ;
* distingués des régressions introduites.

---

# 23. Stratégie Docker

L'infrastructure MVP reste simple :

```text
docker-compose.yml
│
├── postgres
├── backend
└── frontend
```

Ne pas introduire sans besoin réel :

* worker ;
* Redis ;
* Celery ;
* queue ;
* reverse proxy complexe ;
* orchestration distribuée.

Le repository ayant désormais :

```text
pyproject.toml
uv.lock
```

à la racine, les builds Docker nécessitant ces fichiers doivent utiliser des contextes compatibles avec cette organisation.

Les Dockerfiles et `docker-compose.yml` doivent tenir compte de :

```text
src/backend/
src/frontend/
pyproject.toml
uv.lock
```

et ne doivent pas supposer l'ancienne présence de :

```text
backend/
frontend/
backend/pyproject.toml
```

Les chemins `COPY`, les contextes de build et les volumes doivent correspondre à l'arborescence réelle.

---

# 24. Configuration

La configuration importante doit être externalisée.

Exemples :

```text
APP_ENV
DATABASE_URL
LOG_LEVEL

SCRAPER_TIMEOUT
SCRAPER_DELAY

MATCHING_THRESHOLD

COLLECTION_INTERVAL

AI_PROVIDER
AI_MODEL
```

Toutes les variables ne doivent pas nécessairement exister dès le MVP initial.

Ajouter uniquement les variables nécessaires aux fonctionnalités réellement implémentées.

Utiliser :

```text
.env
.env.example
Pydantic Settings
```

Aucun secret réel ne doit être versionné.

---

# 25. Gestion des erreurs

L'application utilise une stratégie centralisée d'erreurs.

Les exceptions métier ou applicatives doivent pouvoir être transformées en réponses HTTP cohérentes à la frontière API.

Architecture :

```text
Domain / Application
        │
        ▼
ApplicationError
        │
        ▼
FastAPI exception handler
        │
        ▼
HTTP error response
```

Les services métier ne doivent pas dépendre inutilement de `HTTPException`.

Les stack traces ne doivent pas être exposées au frontend.

---

# 26. Transactions

Les opérations modifiant plusieurs entités liées doivent rester atomiques.

Exemple :

```text
update profile
     +
update skills
     +
update technologies
     +
update preferences
     ↓
single transaction
```

En cas d'erreur :

```text
ROLLBACK
```

Les frontières transactionnelles doivent être explicites et cohérentes.

---

# 27. Observabilité

Le MVP utilise des logs simples et structurés.

Les logs doivent permettre de suivre notamment :

* démarrage de collecte ;
* fin de collecte ;
* nombre d'offres ;
* nouvelles offres ;
* erreurs de source ;
* doublons ;
* matching ;
* erreurs applicatives.

Les logs ne doivent pas contenir inutilement :

* secrets ;
* CV ;
* profil complet ;
* informations personnelles sensibles.

Une infrastructure complète de monitoring distribué n'est pas nécessaire au MVP.

---

# 28. Sécurité et confidentialité

Les données suivantes sont considérées comme sensibles :

* profil ;
* préférences ;
* CV futur ;
* candidatures ;
* interactions ;
* informations personnelles.

Principes :

* secrets hors du code ;
* validation des entrées ;
* contrôle des uploads futurs ;
* aucune donnée sensible inutile dans les logs ;
* minimisation des données envoyées à des services externes ;
* configuration locale possible lorsque pertinent.

L'authentification peut rester hors MVP tant que l'application est strictement locale.

Elle devra être reconsidérée avant toute exposition réseau non maîtrisée.

---

# 29. Architecture IA future

Les fonctionnalités IA sont post-MVP.

Architecture conceptuelle future :

```text
JobOffer
   │
   ├── deterministic extraction
   ├── NLP
   ├── embeddings
   └── LLM optional
          │
          ▼
Structured enrichment
```

Lorsque ces fonctions seront implémentées, utiliser des abstractions telles que :

```text
EmbeddingProvider
LLMProvider
JobInformationExtractor
```

uniquement lorsqu'elles deviennent réellement nécessaires.

Éviter les abstractions prématurées.

---

# 30. Recherche sémantique future

La première approche prévue est :

```text
PostgreSQL
+
pgvector
```

plutôt qu'une base vectorielle séparée.

La recherche pourra combiner :

```text
filtres structurés
+
recherche textuelle
+
similarité vectorielle
```

Cette fonctionnalité ne doit pas influencer inutilement le modèle du MVP avant son étape dédiée.

---

# 31. Principaux risques

## 31.1 Sur-ingénierie

Risque :

> créer trop de couches avant que le besoin existe.

Réponse :

* architecture pragmatique ;
* petites étapes ;
* abstractions uniquement utilisées.

---

## 31.2 Fragilité des sources

Les sites externes peuvent changer ou devenir indisponibles.

Réponse :

* adapters isolés ;
* fixtures ;
* gestion d'erreurs ;
* sources indépendantes.

---

## 31.3 Perte d'information

Une normalisation trop agressive peut supprimer des informations utiles.

Réponse :

* conservation des snapshots ;
* conservation des valeurs brutes pertinentes.

---

## 31.4 Faux positifs de déduplication

Une fusion incorrecte peut masquer deux offres réellement différentes.

Réponse :

* approche conservatrice ;
* plusieurs niveaux de preuve ;
* provenance conservée.

---

## 31.5 Matching opaque

Un score incompréhensible réduit la confiance dans l'application.

Réponse :

* moteur déterministe V1 ;
* composantes visibles ;
* versionnement ;
* explications basées sur les règles réelles.

---

## 31.6 Données personnelles

Le profil, les candidatures et le futur CV contiennent des informations sensibles.

Réponse :

* minimisation ;
* confidentialité ;
* services externes optionnels ;
* logs prudents.

---

## 31.7 Dérive de la roadmap par l'agent

Un agent peut vouloir regrouper plusieurs fonctionnalités ou anticiper les étapes suivantes.

Réponse :

* `docs/ROADMAP.md` comme source de vérité ;
* `.github/copilot-instructions.md` comme contrat permanent ;
* une étape à la fois ;
* pas de changement silencieux de roadmap.

---

# 32. Principes de décision architecturale

Pour toute décision structurante :

```text
Décision
Pourquoi
Alternative écartée
Quand reconsidérer
```

Les décisions réellement significatives doivent être enregistrées sous :

```text
docs/adr/
```

Ne pas créer d'ADR pour des détails triviaux.

---

# 33. Décisions actuellement retenues

Les décisions fondamentales actuelles sont :

* monolithe modulaire ;
* backend Python / FastAPI ;
* frontend React + TypeScript + Vite ;
* PostgreSQL comme source de vérité ;
* SQLAlchemy 2 ;
* Alembic ;
* Pydantic v2 ;
* uv à la racine du repository ;
* `pyproject.toml` et `uv.lock` à la racine ;
* backend sous `src/backend/` ;
* frontend sous `src/frontend/` ;
* code applicatif backend sous `src/backend/app/` ;
* tests backend sous `src/backend/tests/` ;
* Ruff + ty uniquement sur le code applicatif backend ;
* pytest pour les tests backend ;
* matching V1 déterministe ;
* déduplication non destructive ;
* collecte indépendante du matching ;
* absence de Redis/Celery/microservices pour le MVP ;
* Docker local simple ;
* fonctionnalités IA après validation du MVP.

---

# 34. Principe final

Toutes les décisions doivent rester alignées sur la question :

> Cette architecture permet-elle de construire de manière simple, fiable, testable et compréhensible un système capable d'identifier les offres les plus pertinentes pour l'utilisateur ?

Lorsque deux solutions satisfont le besoin, préférer :

```text
simple > complexe
explicite > implicite
déterministe > opaque
testable > supposé
progressif > massif
réversible > destructif
maintenable > ingénieux
```

L'objectif n'est pas de construire l'architecture la plus sophistiquée.

L'objectif est de construire **la plus petite architecture fiable permettant au produit d'évoluer proprement**.
