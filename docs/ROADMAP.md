# Roadmap — Job Finder

## Statut du projet

Le projet est développé de manière incrémentale.

Chaque étape doit rester suffisamment petite pour pouvoir être :

* comprise ;
* implémentée ;
* testée ;
* relue ;
* validée ;
* commitée indépendamment.

Une étape suivante ne doit pas être commencée automatiquement.

Une étape peut être considérée comme terminée lorsque :

1. ses critères essentiels sont satisfaits ;
2. les régressions introduites par l'étape sont corrigées ;
3. les limitations restantes sont explicitement documentées ;
4. les validations applicables ont été réellement exécutées.

Les fonctionnalités post-MVP ne doivent pas complexifier prématurément l'architecture du MVP.

---

# Vue d'ensemble

| Étape | Description                                         | État       |
| ----- | --------------------------------------------------- | ---------- |
| 0     | Architecture                                        | ✅ Terminée |
| 1     | Bootstrap du repository                             | ✅ Terminée |
| 2     | Infrastructure locale Docker/PostgreSQL             | ✅ Terminée |
| 3     | Modèle de données initial et persistance            | ✅ Terminée |
| 4     | Fondation API FastAPI                               | ✅ Terminée |
| 5     | Profil utilisateur et préférences                   | ✅ Terminée |
| 6     | Domaine et API des offres                           | ✅ Terminée |
| 7     | Collecteur fictif                                   | ✅ Terminée |
| 8     | Pipeline collecte → normalisation → stockage        | ✅ Terminée |
| 9     | Déduplication                                       | ✅ Terminée |
| 10    | Premier connecteur réel                             | ⬜ À faire  |
| 11    | Matching déterministe V1                            | ⬜ À faire  |
| 12    | Frontend — liste et détail des offres               | ⬜ À faire  |
| 13    | Frontend — profil et préférences                    | ⬜ À faire  |
| 14    | Favoris, rejets et archivage                        | ⬜ À faire  |
| 15    | Suivi des candidatures                              | ⬜ À faire  |
| 16    | Import et analyse du CV                             | ⬜ Post-MVP |
| 17    | Enrichissement NLP                                  | ⬜ Post-MVP |
| 18    | Embeddings et pgvector                              | ⬜ Post-MVP |
| 19    | Recherche sémantique                                | ⬜ Post-MVP |
| 20    | Matching hybride et personnalisation                | ⬜ Post-MVP |
| 21    | Scheduler de collecte                               | ⬜ Post-MVP |
| 22    | Alertes                                             | ⬜ Post-MVP |
| 23    | Stabilisation, optimisation et documentation finale | ⬜ Post-MVP |

---

# Phase A — Fondations techniques

## Étape 0 — Architecture

**État : ✅ TERMINÉE**

### Objectif

Transformer la spécification produit en une architecture cohérente, maintenable et adaptée à un MVP personnel.

### Réalisé

* architecture de monolithe modulaire définie ;
* périmètre du MVP défini ;
* structure du repository définie ;
* domaines backend et responsabilités identifiés ;
* modèle de données initial défini ;
* pipeline général de collecte défini ;
* stratégie de normalisation définie ;
* stratégie de déduplication définie ;
* stratégie de matching déterministe définie ;
* stratégie de tests définie ;
* stratégie Docker définie ;
* décisions structurantes documentées ;
* ADRs créés dans `docs/adr/`.

### Documentation principale

* `docs/ARCHITECTURE.md`
* `docs/PROJECT_SPEC.md`
* `docs/adr/`

### Critères de validation

* [x] architecture globale documentée ;
* [x] MVP clairement délimité ;
* [x] responsabilités principales séparées ;
* [x] décisions structurantes documentées.

---

## Étape 1 — Bootstrap du repository

**État : ✅ TERMINÉE**

### Objectif

Mettre en place le squelette technique initial du projet et la chaîne de qualité.

### Réalisé

* backend Python ;
* frontend React + TypeScript + Vite ;
* `pyproject.toml` ;
* `uv.lock` ;
* gestion des dépendances Python avec `uv` ;
* Ruff configuré ;
* ty configuré ;
* pytest configuré ;
* TypeScript strict ;
* `.gitignore` ;
* `.env.example` ;
* documentation de développement initiale.

### Organisation actuelle

Le projet a depuis été réorganisé sous :

```text
/
├── pyproject.toml
├── uv.lock
│
└── src/
    ├── backend/
    │   ├── app/
    │   └── tests/
    │
    └── frontend/
```

Le repository root constitue la racine du projet Python.

### Outils Python retenus

* `uv` — projet, environnement et dépendances ;
* Ruff — linting et formatage du code applicatif ;
* ty — vérification statique du code applicatif ;
* pytest — tests backend.

### Critères de validation

* [x] structure backend créée ;
* [x] structure frontend créée ;
* [x] dépendances Python gérées avec `uv` ;
* [x] `uv.lock` présent ;
* [x] Ruff fonctionnel ;
* [x] ty fonctionnel ;
* [x] pytest fonctionnel ;
* [x] TypeScript strict configuré.

---

## Étape 2 — Infrastructure locale

**État : ✅ TERMINÉE**

### Objectif

Permettre un démarrage local reproductible de l'application avec Docker et PostgreSQL.

### Réalisé

* `docker-compose.yml` ;
* service PostgreSQL ;
* service backend ;
* service frontend ;
* Dockerfile backend ;
* Dockerfile frontend ;
* volume persistant PostgreSQL ;
* variables Docker/PostgreSQL ;
* `.env.example` ;
* health checks ;
* configuration cohérente backend/PostgreSQL ;
* documentation de développement locale.

### Inclus

* PostgreSQL ;
* backend ;
* frontend ;
* configuration d'environnement ;
* health checks ;
* volumes locaux.

### Explicitement non inclus

* Redis ;
* Celery ;
* worker séparé ;
* Elasticsearch ;
* Kubernetes ;
* infrastructure cloud ;
* logique métier.

### Critères de validation

* [x] Docker Compose configuré ;
* [x] PostgreSQL configuré ;
* [x] backend conteneurisé ;
* [x] frontend conteneurisé ;
* [x] variables d'environnement documentées ;
* [x] health checks configurés.

### Point de vigilance

Toute évolution de l'organisation du repository doit préserver la cohérence des :

* contexts Docker ;
* chemins `COPY` ;
* volumes ;
* chemins vers `pyproject.toml` et `uv.lock`.

---

## Étape 3 — Modèle de données initial et persistance

**État : ✅ TERMINÉE**

### Objectif

Mettre en place la couche de persistence PostgreSQL avec SQLAlchemy 2 et Alembic.

### Réalisé

#### Configuration

* configuration centralisée ;
* `DATABASE_URL` ;
* `APP_ENV` ;
* `LOG_LEVEL`.

#### SQLAlchemy

* `DeclarativeBase` ;
* engine SQLAlchemy ;
* `SessionLocal` ;
* gestion centralisée des sessions ;
* dépendance de session réutilisable.

#### Modèles initiaux

* `JobSource` ;
* `RawJobSnapshot` ;
* `JobOffer` ;
* `JobSourceOccurrence`.

Ces modèles constituent la base structurelle de la gestion des offres et de leur provenance.

#### Alembic

* Alembic relié à la metadata SQLAlchemy ;
* migration initiale créée.

#### Tests

* tests de configuration de persistence ;
* tests des modèles SQLAlchemy.

### Principes architecturaux validés

* PostgreSQL est la source de vérité ;
* les données brutes sont séparées des offres canonisées ;
* une offre canonique peut avoir plusieurs occurrences ;
* la déduplication sera non destructive ;
* les migrations sont gérées avec Alembic ;
* `Base.metadata.create_all()` ne remplace pas Alembic dans le fonctionnement normal.

### Critères de validation

* [x] SQLAlchemy configuré ;
* [x] gestion des sessions centralisée ;
* [x] modèles initiaux créés ;
* [x] metadata Alembic configurée ;
* [x] migration initiale créée ;
* [x] tests de persistence présents.

---

## Étape 4 — Fondation API FastAPI

**État : ✅ TERMINÉE**

### Objectif

Mettre en place une fondation HTTP propre, robuste et extensible avant l'ajout des fonctionnalités métier.

### Réalisé

#### Application

* application factory `create_app()` ;
* point d'entrée FastAPI ;
* routeur principal ;
* versionnement `/api/v1`.

#### Santé

* `GET /health` ;
* `GET /health/ready` ;
* vérification de disponibilité de PostgreSQL pour la readiness.

#### Persistence

* dépendance FastAPI d'injection de session SQLAlchemy.

#### Gestion des erreurs

Hiérarchie initiale :

* `ApplicationError` ;
* `DatabaseError` ;
* `ServiceUnavailableError`.

Gestion centralisée des exceptions avec un format API cohérent.

#### Configuration HTTP

* CORS ;
* développement frontend local supporté.

#### Documentation

* OpenAPI ;
* Swagger UI ;
* ReDoc.

#### Tests

* tests de création de l'application ;
* tests OpenAPI ;
* tests des endpoints de santé ;
* tests de gestion centralisée des erreurs.

### Explicitement non inclus

* domaine des offres ;
* candidatures ;
* collecte ;
* normalisation ;
* déduplication ;
* matching ;
* authentification ;
* NLP.

### Critères de validation

* [x] application factory fonctionnelle ;
* [x] routeur versionné ;
* [x] endpoints de santé ;
* [x] injection des sessions ;
* [x] gestion centralisée des erreurs ;
* [x] OpenAPI disponible ;
* [x] tests API fondamentaux présents.

---

# Phase B — Domaines métier

## Étape 5 — Profil utilisateur et préférences

**État : ✅ TERMINÉE**

### Objectif

Créer la première fonctionnalité métier complète de l'application : le profil utilisateur et ses préférences de recherche.

Le profil constitue la référence structurée qui sera utilisée ultérieurement par le moteur de matching.

### Réalisé

* profil utilisateur mono-utilisateur ;
* persistence SQLAlchemy du profil ;
* relations et données structurées associées ;
* compétences ;
* technologies ;
* langues ;
* préférences ;
* schémas Pydantic de lecture/écriture ;
* validation des entrées ;
* endpoint :

```text
GET /api/v1/profile
```

* endpoint :

```text
PUT /api/v1/profile
```

* comportement explicite lorsque le profil n'existe pas ;
* remplacement idempotent du profil ;
* mise à jour transactionnelle des relations ;
* tests API du profil ;
* test de régression sur les PUT successifs.

### Stratégie mono-utilisateur

L'application gère actuellement un unique profil utilisateur actif.

Aucun système de :

* comptes ;
* login ;
* JWT ;
* rôles ;
* permissions

n'est nécessaire pour le MVP local.

### Comportement API actuel

Si aucun profil n'existe :

```text
GET /api/v1/profile
```

retourne :

```text
404 PROFILE_NOT_FOUND
```

Le `PUT` est idempotent.

Des requêtes identiques répétées ne doivent pas créer de doublons dans les données enfants.

### Correctif de régression important

Un problème a été identifié lors de PUT successifs :

> les lignes enfants associées au profil pouvaient rester persistées et provoquer des doublons sur les contraintes uniques.

La stratégie retenue remplace explicitement les relations concernées dans la même opération transactionnelle avant de persister l'état canonique du profil.

### Explicitement non inclus

* frontend du profil ;
* import CV ;
* matching ;
* apprentissage automatique des préférences ;
* recommandations ;
* NLP.

### Critères de validation

* [x] modèle de profil créé ;
* [x] préférences structurées ;
* [x] persistence fonctionnelle ;
* [x] schémas Pydantic créés ;
* [x] lecture du profil fonctionnelle ;
* [x] modification du profil fonctionnelle ;
* [x] PUT idempotent ;
* [x] absence de duplication lors des remplacements ;
* [x] gestion du profil absent ;
* [x] tests de régression présents ;
* [x] tests ciblés du profil passants ;
* [x] documentation mise à jour.

---

## Étape 6 — Domaine et API des offres

**État : ✅ TERMINÉE**

### Objectif

Transformer les modèles de persistence `JobOffer` existants en véritable domaine consultable par l'API.

Cette étape travaille sur des offres déjà présentes en base.

Elle ne collecte encore aucune donnée externe.

### Inclus

* schémas Pydantic des offres ;
* API de consultation des offres sous `/api/v1/jobs` ;
* endpoint de détail sous `/api/v1/jobs/{id}` ;
* pagination déterministe ;
* filtres initiaux applicables aux champs existants ;
* tri explicite et limité ;
* gestion des offres inexistantes ;
* exposition contrôlée de la provenance via `JobSourceOccurrence` ;
* tests API deterministes ;
* validation des réponses structurelles.

### Pagination

La pagination est implémentée sous la forme :

```text
page
page_size
total
items
```

Le `page_size` est borné raisonnablement et les paramètres invalides sont rejetés par validation FastAPI.

La pagination est appliquée après les filtres.

### Filtres initiaux possibles

Uniquement selon les champs réellement disponibles dans `JobOffer` :

* entreprise ;
* ville ;
* pays ;
* type de contrat ;
* type de poste ;
* remote ;
* statut ;
* date de publication.

Les filtres sont combinables.

### Tri

Prévoir un ensemble fermé de tris autorisés.

Exemples possibles :

* date de publication ;
* date de création ;
* titre.

Ne jamais transformer directement une valeur arbitraire fournie par l'utilisateur en nom de colonne SQL.

### Provenance

Le détail d'une offre peut exposer les informations pertinentes issues de `JobSourceOccurrence`, telles que :

* source ;
* identifiant externe ;
* URL originale.

Les `RawJobSnapshot` ne doivent pas être exposés directement par défaut dans l'API métier.

### Explicitement non inclus

* collecteur ;
* scraping ;
* normalisation ;
* déduplication ;
* matching ;
* recherche sémantique ;
* frontend métier ;
* favoris.

### Critères de validation

* [x] schémas Pydantic définis ;
* [x] liste paginée fonctionnelle ;
* [x] détail d'une offre fonctionnel ;
* [x] filtres essentiels fonctionnels ;
* [x] tri contrôlé ;
* [x] provenance exposée lorsque pertinente ;
* [x] erreurs API cohérentes ;
* [x] tests présents ;
* [x] aucune régression introduite ;
* [x] quality gate applicable validé.

---

# Phase C — Acquisition et traitement des offres

## Étape 7 — Collecteur fictif

**État : ✅ TERMINÉE**

### Objectif

Créer une source entièrement locale permettant de tester le système sans dépendre d'un site externe.

### Inclus

* abstraction commune des sources ;
* `FakeJobSource` ou équivalent ;
* fixtures réalistes ;
* cas volontairement incomplets ;
* offres avec différents contrats et localisations ;
* offres similaires pour préparer la déduplication ;
* données brutes en mémoire ;
* tests déterministes.

### Jeu de données fictif

Les fixtures doivent notamment permettre de représenter :

* offre classique ;
* remote ;
* hybride ;
* différentes villes ;
* différents contrats ;
* salaire absent ;
* expérience absente ;
* technologies différentes ;
* offres potentiellement dupliquées.

### Explicitement non inclus

* connexion à un site externe ;
* scraping réel ;
* Playwright ;
* déduplication effective ;
* matching ;
* pipeline collecte → normalisation → stockage.

### Critères de validation

* [x] abstraction de source définie ;
* [x] collecteur fictif fonctionnel ;
* [x] fixtures déterministes ;
* [x] données brutes produites ;
* [x] aucune dépendance réseau dans les tests ;
* [x] quality gate applicable validé.

---

## Étape 8 — Pipeline collecte → normalisation → stockage

**État : ✅ TERMINÉE**

### Objectif

Créer le premier pipeline complet de traitement d'une offre.

### Pipeline cible

```text
collect
   ↓
RawJob
   ↓
RawJobSnapshot
   ↓
parse
   ↓
normalize
   ↓
JobOfferCandidate
   ↓
persist
```

### Inclus

* orchestration du pipeline ;
* validation des données brutes ;
* parsing ;
* normalisation ;
* snapshots ;
* persistence des offres ;
* gestion des erreurs partielles ;
* logs ;
* tests du pipeline.

### Normalisation initiale

Prévoir notamment :

* titre ;
* entreprise ;
* URL ;
* localisation ;
* pays ;
* ville ;
* contrat ;
* remote ;
* dates ;
* salaire lorsque disponible.

### Explicitement non inclus

* déduplication avancée ;
* source réelle ;
* matching ;
* NLP.

### Critères de validation

* [x] pipeline complet fonctionnel avec le collecteur fictif ;
* [x] snapshots conservés ;
* [x] offres normalisées persistées ;
* [x] erreur sur une offre n'arrêtant pas nécessairement tout le batch ;
* [x] tests d'intégration présents ;
* [x] quality gate applicable validé.

---

## Étape 9 — Déduplication

**État : ✅ TERMINÉE**

### Objectif

Identifier plusieurs occurrences représentant probablement la même offre sans perte de provenance.

### Stratégie

Déduplication progressive :

1. identifiants forts ;
2. URL canonique ;
3. hash exact ;
4. fingerprint déterministe ;
5. similarité floue si nécessaire.

### Résultats conceptuels

```text
NOT_DUPLICATE
POSSIBLE_DUPLICATE
CONFIRMED_DUPLICATE
```

### Principe fondamental

Une occurrence source ne doit pas être détruite lorsqu'elle correspond à une offre déjà connue.

Elle doit être reliée à l'offre canonique.

### Inclus

* fingerprints ;
* normalisation nécessaire aux comparaisons ;
* stratégie de décision ;
* association aux offres canoniques ;
* tests de doublons ;
* tests de faux positifs ;
* tests de faux négatifs.

### Explicitement non inclus

* embeddings ;
* similarité vectorielle ;
* LLM ;
* matching utilisateur.

### Critères de validation

* [x] doublons exacts détectés ;
* [x] provenance conservée ;
* [x] cas ambigus traités de façon conservatrice ;
* [x] tests des cas limites ;
* [x] quality gate applicable validé.

### Limitation connue

La décision `POSSIBLE_DUPLICATE` (correspondance par fingerprint déterministe) est actuellement traitée par le pipeline exactement comme `NOT_DUPLICATE` : une nouvelle offre canonique distincte est créée, sans lien ni file de révision vers l'offre similaire existante.

Ce comportement respecte le principe conservateur (aucune fusion agressive), mais l'information `POSSIBLE_DUPLICATE` n'est pas encore exploitée. Une évolution future pourra introduire une file de révision si les faux négatifs deviennent un problème réel.

---

## Étape 10 — Premier connecteur réel

**État : ⬜ À FAIRE**

### Objectif

Brancher une seule source externe réelle sur le pipeline déjà validé.

### Avant toute implémentation

Créer une fiche source :

```text
Source:
URL:
Méthode utilisée:
API officielle:
RSS / feed:
Scraping nécessaire:
robots.txt:
Restrictions connues:
Authentification:
Fréquence recommandée:
Données récupérées:
Date de dernière vérification:
Remarques:
```

### Ordre de préférence

1. API officielle ;
2. feed structuré ;
3. HTTP + parsing ;
4. crawler spécialisé ;
5. navigateur automatisé uniquement si nécessaire et approprié.

### Interdictions

Ne jamais contourner :

* CAPTCHA ;
* authentification ;
* paywalls ;
* protections anti-bot ;
* limitations explicitement destinées à empêcher l'automatisation.

### Inclus

* une seule source réelle ;
* intégration avec l'abstraction existante ;
* timeouts ;
* erreurs réseau ;
* rate limiting raisonnable ;
* fixtures ;
* tests sans dépendance directe au site réel.

### Critères de validation

* [ ] méthode de collecte étudiée et documentée ;
* [ ] fiche source créée ;
* [ ] connecteur isolé du cœur métier ;
* [ ] pipeline existant réutilisé ;
* [ ] tests à base de fixtures ;
* [ ] quality gate applicable validé.

---

# Phase D — Recommandation

## Étape 11 — Matching déterministe V1

**État : ⬜ À FAIRE**

### Objectif

Classer les offres en fonction du profil utilisateur avec un moteur déterministe, configurable et explicable.

### Composantes possibles

* compétences ;
* technologies ;
* localisation ;
* contrat ;
* formation ;
* expérience ;
* langues ;
* remote ;
* industrie ;
* salaire ;
* durée ;
* rôle.

### Critères éliminatoires

Séparer les contraintes bloquantes du score.

Exemples :

* contrat obligatoire ;
* localisation incompatible ;
* durée incompatible ;
* disponibilité ;
* compétence obligatoire ;
* langue obligatoire ;
* rôle exclu.

### Gestion de l'incertitude

Utiliser :

```text
MATCH
MISMATCH
UNKNOWN
```

Une information absente ne doit pas automatiquement être interprétée comme incompatible.

### Versionnement

Le résultat doit conserver la version du moteur.

Exemple :

```text
deterministic-v1
```

### Explicabilité

Retourner notamment :

* score global ;
* composantes ;
* critères bloquants ;
* points forts ;
* points faibles ;
* informations inconnues.

### Explicitement non inclus

* embeddings ;
* LLM ;
* apprentissage automatique ;
* personnalisation comportementale.

### Critères de validation

* [ ] score reproductible ;
* [ ] poids configurables ;
* [ ] critères bloquants ;
* [ ] gestion `UNKNOWN` ;
* [ ] explication dérivée du calcul réel ;
* [ ] version du moteur conservée ;
* [ ] tests unitaires approfondis ;
* [ ] quality gate applicable validé.

---

# Phase E — Frontend MVP

## Étape 12 — Frontend : liste et détail des offres

**État : ⬜ À FAIRE**

### Objectif

Créer la première interface réellement utilisable de consultation des offres.

### Liste

Afficher notamment :

* titre ;
* entreprise ;
* localisation ;
* contrat ;
* remote ;
* date ;
* score lorsqu'il existe ;
* compétences principales.

### Fonctionnalités

* pagination ;
* recherche textuelle simple ;
* filtres ;
* tri ;
* navigation vers le détail ;
* gestion du chargement ;
* gestion des erreurs API.

### Détail

Afficher :

* description ;
* données structurées ;
* provenance ;
* score ;
* explication ;
* points forts ;
* points faibles ;
* informations inconnues ;
* URL source.

### Explicitement non inclus

* profil frontend ;
* candidatures ;
* recherche sémantique.

### Critères de validation

* [ ] liste fonctionnelle ;
* [ ] pagination ;
* [ ] filtres ;
* [ ] détail fonctionnel ;
* [ ] erreurs API correctement affichées ;
* [ ] tests frontend principaux.

---

## Étape 13 — Frontend : profil et préférences

**État : ⬜ À FAIRE**

### Objectif

Permettre de consulter et modifier le profil depuis l'interface.

### Inclus

* formulaire de profil ;
* compétences ;
* technologies ;
* langues ;
* localisation ;
* mobilité ;
* contrats ;
* préférences ;
* critères obligatoires ;
* exclusions ;
* validation frontend ;
* synchronisation API.

### Explicitement non inclus

* import CV ;
* apprentissage automatique des préférences.

### Critères de validation

* [ ] lecture ;
* [ ] modification ;
* [ ] sauvegarde ;
* [ ] validation ;
* [ ] gestion des erreurs API ;
* [ ] tests frontend principaux.

---

## Étape 14 — Favoris, rejets et archivage

**État : ⬜ À FAIRE**

### Objectif

Permettre à l'utilisateur d'indiquer ses décisions sur les offres.

### Interactions initiales

```text
view
favorite
reject
archive
```

### Inclus

* modèle d'interaction ;
* migration ;
* service ;
* endpoints API ;
* actions frontend ;
* filtres par statut ;
* tests.

### Explicitement non inclus

* apprentissage automatique ;
* modification automatique des préférences.

### Critères de validation

* [ ] favoris persistés ;
* [ ] rejets persistés ;
* [ ] archives persistées ;
* [ ] frontend mis à jour ;
* [ ] tests backend et frontend.

---

## Étape 15 — Suivi des candidatures

**État : ⬜ À FAIRE**

### Objectif

Permettre le suivi complet des candidatures.

### Statuts initiaux

```text
TO_REVIEW
FAVORITE
TO_PREPARE
APPLIED
INTERVIEW
TECHNICAL_TEST
OFFER_RECEIVED
REJECTED
WITHDRAWN
ARCHIVED
```

### Données possibles

* offre ;
* entreprise ;
* poste ;
* date de candidature ;
* statut ;
* date de relance ;
* notes ;
* contacts ;
* prochaine action ;
* référence du CV ;
* référence de la lettre.

### Inclus

* modèle ;
* migration ;
* API ;
* interface ;
* tests.

### Critères de validation

* [ ] création d'une candidature ;
* [ ] modification du statut ;
* [ ] historique minimal cohérent ;
* [ ] relance enregistrable ;
* [ ] interface fonctionnelle ;
* [ ] tests présents.

---

# Frontière MVP

Les Étapes **0 à 15** constituent le chemin vers le MVP fonctionnel.

À l'issue de l'Étape 15, l'application doit être utilisable sans LLM, embeddings ou recherche vectorielle.

Le flux principal doit fonctionner :

```text
Source réelle
   ↓
Collecte
   ↓
RawJobSnapshot
   ↓
Normalisation
   ↓
Déduplication
   ↓
JobOffer canonique
   ↓
Matching déterministe
   ↓
Classement
   ↓
Consultation frontend
   ↓
Favoris / rejets
   ↓
Suivi des candidatures
```

Les fonctionnalités post-MVP ne doivent pas être nécessaires au fonctionnement de ce flux.

---

# Phase F — Évolutions post-MVP

## Étape 16 — Import et analyse du CV

**État : ⬜ POST-MVP**

### Objectif

Importer un CV et proposer des informations structurées à intégrer au profil.

### Inclus

* PDF ;
* DOCX ;
* extraction texte ;
* expériences ;
* formations ;
* compétences ;
* technologies ;
* langues ;
* projets ;
* certifications ;
* validation utilisateur.

### Principe

Le CV peut compléter le profil mais ne doit jamais l'écraser automatiquement.

---

## Étape 17 — Enrichissement NLP

**État : ⬜ POST-MVP**

### Objectif

Améliorer l'extraction structurée des annonces.

### Cibles

* compétences ;
* technologies ;
* missions ;
* langues ;
* expérience ;
* niveau d'étude ;
* catégories de poste.

Privilégier les méthodes déterministes ou locales lorsqu'elles suffisent.

---

## Étape 18 — Embeddings et pgvector

**État : ⬜ POST-MVP**

### Objectif

Introduire une représentation vectorielle des offres et éventuellement du profil.

### Architecture cible

```text
PostgreSQL
+
pgvector
```

### Inclus

* pgvector ;
* stratégie d'embeddings ;
* abstraction `EmbeddingProvider` ;
* stockage ;
* versionnement du modèle ;
* recalcul contrôlé.

Ne pas introduire une base vectorielle séparée sans besoin démontré.

---

## Étape 19 — Recherche sémantique

**État : ⬜ POST-MVP**

### Objectif

Permettre une recherche en langage naturel combinant plusieurs signaux.

### Approche

```text
filtres structurés
+
recherche textuelle
+
similarité vectorielle
```

---

## Étape 20 — Matching hybride et personnalisation

**État : ⬜ POST-MVP**

### Objectif

Améliorer le classement à partir de signaux sémantiques et du comportement utilisateur.

### Approche

```text
matching déterministe
+
similarité sémantique
+
préférences observées
```

### Principe

Les préférences critiques ne doivent jamais être modifiées automatiquement.

Le système peut proposer un changement nécessitant confirmation.

---

## Étape 21 — Scheduler de collecte

**État : ⬜ POST-MVP**

### Objectif

Automatiser périodiquement la collecte.

### Pipeline

```text
Scheduler
   ↓
Collecte
   ↓
Normalisation
   ↓
Déduplication
   ↓
Enrichissement
   ↓
Matching
```

Commencer avec la solution la plus simple suffisante.

Ne pas introduire Celery/Redis sans besoin concret.

---

## Étape 22 — Alertes

**État : ⬜ POST-MVP**

### Objectif

Notifier l'utilisateur lorsqu'une offre particulièrement pertinente apparaît.

### Canaux possibles

* notification interne ;
* email ;
* autres intégrations.

### Contraintes

* seuil configurable ;
* pas de notifications répétées inutilement ;
* alertes désactivables.

---

## Étape 23 — Stabilisation, optimisation et documentation finale

**État : ⬜ POST-MVP**

### Objectif

Stabiliser l'ensemble du système après validation fonctionnelle.

### Axes

* tests ;
* cas limites ;
* performance ;
* index PostgreSQL ;
* sécurité ;
* logs ;
* erreurs ;
* UX ;
* documentation ;
* nettoyage architectural ;
* suppression des abstractions devenues inutiles ;
* dépendances ;
* confidentialité.

---

# Quality gate général

Le repository root est la racine du projet Python.

## Code applicatif backend

Le code :

```text
src/backend/app/
```

est contrôlé par :

* Ruff ;
* Ruff format ;
* ty.

## Tests backend

Les tests :

```text
src/backend/tests/
```

sont contrôlés par :

* pytest.

Les tests sont volontairement exclus de Ruff et ty.

## Commandes

Depuis la racine :

```bash
uv lock --check
uv run ruff check src/backend/app
uv run ruff format --check src/backend/app
uv run ty check
uv run pytest src/backend/tests
```

Une étape ne doit pas introduire de nouvelles erreurs dans ces contrôles.

Si le quality gate révèle des erreurs, elles doivent être classées comme :

1. introduites ou affectées par l'étape courante ;
2. préexistantes et indépendantes ;
3. d'origine incertaine.

Les erreurs appartenant à la première catégorie doivent être corrigées avant validation.

Une erreur ne doit jamais être déclarée « hors périmètre » uniquement parce qu'elle se trouve dans un autre fichier.

Pour les étapes frontend, exécuter également les contrôles TypeScript, lint et tests réellement configurés dans le frontend.

Ne jamais déclarer une commande comme réussie si elle n'a pas été exécutée.

---

# Règles de progression

## Avant une étape

1. lire `.github/copilot-instructions.md` ;
2. lire `docs/PROJECT_SPEC.md` ;
3. lire `docs/ARCHITECTURE.md` ;
4. lire `docs/ROADMAP.md` ;
5. lire `docs/DEVELOPMENT.md` lorsque pertinent ;
6. inspecter l'état réel du repository.

## Pendant une étape

1. respecter strictement le périmètre ;
2. éviter les fonctionnalités futures ;
3. faire la plus petite modification cohérente ;
4. ajouter les tests correspondants ;
5. maintenir la qualité du code applicatif ;
6. documenter les décisions réellement structurantes.

## À la fin d'une étape

1. exécuter les validations applicables ;
2. corriger les régressions introduites ;
3. mettre à jour cette roadmap ;
4. documenter les limitations ;
5. inspecter `git diff` ;
6. créer un commit cohérent ;
7. s'arrêter.

La prochaine étape ne doit jamais être implémentée automatiquement.

---

# État actuel

```text
Étape 0   ✅ Architecture
Étape 1   ✅ Bootstrap
Étape 2   ✅ Infrastructure locale
Étape 3   ✅ Persistence
Étape 4   ✅ Fondation FastAPI
Étape 5   ✅ Profil utilisateur
────────────────────────────────────────
Étape 6   ⬜ Domaine/API offres
Étape 7   ⬜ Collecteur fictif
Étape 8   ✅ Pipeline
Étape 9   ✅ Déduplication
Étape 10  ⬜ Première source réelle     ← PROCHAINE ÉTAPE
Étape 11  ⬜ Matching V1
Étape 12  ⬜ Frontend offres
Étape 13  ⬜ Frontend profil
Étape 14  ⬜ Interactions
Étape 15  ⬜ Candidatures
────────────────────────────────────────
                 MVP
────────────────────────────────────────
Étape 16  ⬜ CV
Étape 17  ⬜ NLP
Étape 18  ⬜ Embeddings / pgvector
Étape 19  ⬜ Recherche sémantique
Étape 20  ⬜ Matching hybride
Étape 21  ⬜ Scheduler
Étape 22  ⬜ Alertes
Étape 23  ⬜ Stabilisation
```

**Prochaine étape autorisée : Étape 6 — Domaine et API des offres.**
