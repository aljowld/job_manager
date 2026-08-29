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

Le projet ne doit pas avancer vers l'étape suivante tant que :

1. les critères essentiels de validation de l'étape courante ne sont pas satisfaits ; ou
2. les limitations restantes ne sont pas explicitement documentées et acceptées.

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
| 6     | Domaine et API des offres                           | ⬜ À faire  |
| 7     | Collecteur fictif                                   | ⬜ À faire  |
| 8     | Pipeline collecte → normalisation → stockage        | ⬜ À faire  |
| 9     | Déduplication                                       | ⬜ À faire  |
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
* structure cible du repository établie ;
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

### Outils Python retenus

* `uv` — projet, environnement et dépendances ;
* `ruff` — linting et formatage ;
* `ty` — vérification statique des types ;
* `pytest` — tests backend.

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
* `Dockerfile.backend` ;
* `Dockerfile.frontend` ;
* volume persistant PostgreSQL ;
* variables Docker/PostgreSQL ;
* `.env.example` ;
* health checks ;
* configuration cohérente entre backend et PostgreSQL ;
* documentation de démarrage Docker et local.

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

---

## Étape 3 — Modèle de données initial et persistance

**État : ✅ TERMINÉE**

### Objectif

Mettre en place la couche de persistance PostgreSQL avec SQLAlchemy 2 et Alembic.

### Réalisé

#### Configuration

* configuration centralisée via `config.py` ;
* `DATABASE_URL` ;
* `APP_ENV` ;
* `LOG_LEVEL`.

#### SQLAlchemy

* `DeclarativeBase` ;
* engine SQLAlchemy ;
* `SessionLocal` ;
* gestion centralisée des sessions ;
* dépendance `get_db()`.

#### Modèles initiaux

* `JobSource` ;
* `RawJobSnapshot` ;
* `JobOffer` ;
* `JobSourceOccurrence`.

Ces modèles constituent la base structurelle de la gestion future des offres et de leur provenance.

#### Alembic

* Alembic relié à la metadata SQLAlchemy ;
* migration initiale créée :

  * `20240829_000001_initial_persistence_schema.py`.

#### Tests

* `test_persistence_setup.py` ;
* tests des modèles et de la configuration de persistence.

### Principes architecturaux validés

* PostgreSQL est la source de vérité ;
* les données brutes peuvent être conservées indépendamment des offres normalisées ;
* une offre canonique peut avoir plusieurs occurrences provenant de plusieurs sources ;
* la déduplication future ne devra pas supprimer destructivement les occurrences sources ;
* les migrations sont gérées avec Alembic et non avec `Base.metadata.create_all()` en production.

### Critères de validation

* [x] SQLAlchemy configuré ;
* [x] gestion des sessions centralisée ;
* [x] modèles initiaux créés ;
* [x] metadata Alembic configurée ;
* [x] migration initiale créée ;
* [x] tests de persistence présents ;
* [x] Ruff valide ;
* [x] ty valide ;
* [x] pytest valide.

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
* vérification de disponibilité de la base pour la readiness.

#### Persistence

* dépendance FastAPI `get_db()` ;
* injection des sessions SQLAlchemy.

#### Gestion des erreurs

Hiérarchie initiale :

* `ApplicationError` ;
* `DatabaseError` ;
* `ServiceUnavailableError`.

Gestion centralisée des exceptions avec format de réponse API cohérent.

#### Configuration HTTP

* CORS ;
* `localhost:5173` ;
* `localhost:3000`.

#### Documentation API

* OpenAPI ;
* Swagger UI ;
* ReDoc.

#### Tests

* `test_api_setup.py` ;
* `test_error_handling.py` ;
* `test_health.py`.

### Validations réalisées

* [x] `uv lock --check` ;
* [x] `uv run ruff check .` ;
* [x] formatage Ruff ;
* [x] `uv run ty check` ;
* [x] `uv run pytest` ;
* [x] 12 tests passants ;
* [x] démarrage FastAPI validé.

### Explicitement non inclus

* endpoints métier des offres ;
* profil utilisateur ;
* candidatures ;
* collecte ;
* normalisation ;
* déduplication ;
* matching ;
* authentification ;
* NLP.

---

# Phase B — Premier domaine métier

## Étape 5 — Profil utilisateur et préférences

**État : ⬜ À FAIRE**

### Objectif

Créer la première fonctionnalité métier complète de l'application : le profil utilisateur et ses préférences de recherche.

Le profil doit constituer la référence structurée utilisée ultérieurement par le moteur de matching.

### Inclus

* modèle `UserProfile` ;
* modèle de préférences ;
* migrations Alembic ;
* schémas Pydantic ;
* repository ou service de persistence si nécessaire ;
* logique applicative du profil ;
* endpoints :

  * `GET /api/v1/profile`
  * `PUT /api/v1/profile`
* tests unitaires ;
* tests d'intégration API/base de données.

### Données à prévoir progressivement

* formation ;
* diplômes ;
* expériences ;
* compétences ;
* technologies ;
* langues ;
* localisation ;
* mobilité ;
* préférence remote ;
* types de contrat ;
* types de poste ;
* industries ;
* rôles préférés ;
* rôles exclus ;
* salaire souhaité ;
* disponibilité ;
* durée de stage ;
* entreprises préférées ;
* entreprises exclues.

### Niveaux de préférence

Prévoir conceptuellement :

* `REQUIRED`
* `VERY_IMPORTANT`
* `IMPORTANT`
* `BONUS`
* `AVOID`
* `EXCLUDED`

Les préférences simples, les critères obligatoires et les critères éliminatoires doivent rester distinguables.

### Explicitement non inclus

* interface frontend du profil ;
* import de CV ;
* matching ;
* apprentissage des préférences ;
* recommandations automatiques ;
* NLP.

### Critères de validation

* [ ] modèles créés ;
* [ ] migration créée et applicable ;
* [ ] lecture du profil fonctionnelle ;
* [ ] modification du profil fonctionnelle ;
* [ ] validation Pydantic fonctionnelle ;
* [ ] tests présents ;
* [ ] Ruff valide ;
* [ ] ty valide ;
* [ ] pytest valide ;
* [ ] documentation mise à jour.

---

## Étape 6 — Domaine et API des offres

**État : ⬜ À FAIRE**

### Objectif

Transformer les modèles de persistence `JobOffer` en véritable domaine consultable par l'API.

### Inclus

* schémas Pydantic des offres ;
* repository des offres si nécessaire ;
* service de consultation ;
* pagination ;
* filtres initiaux ;
* tri ;
* endpoint :

  * `GET /api/v1/jobs`
* endpoint :

  * `GET /api/v1/jobs/{id}`
* gestion propre des offres inexistantes ;
* tests API ;
* tests de persistence pertinents.

### Filtres initiaux possibles

* localisation ;
* type de contrat ;
* remote ;
* date de publication ;
* entreprise ;
* statut.

Les filtres avancés pourront être ajoutés progressivement.

### Explicitement non inclus

* scraping ;
* matching ;
* déduplication algorithmique ;
* recherche sémantique ;
* frontend métier.

### Critères de validation

* [ ] liste paginée fonctionnelle ;
* [ ] détail d'une offre fonctionnel ;
* [ ] filtres essentiels fonctionnels ;
* [ ] erreurs API cohérentes ;
* [ ] tests présents ;
* [ ] Ruff valide ;
* [ ] ty valide ;
* [ ] pytest valide.

---

# Phase C — Acquisition et traitement des offres

## Étape 7 — Collecteur fictif

**État : ⬜ À FAIRE**

### Objectif

Créer une source entièrement locale permettant de tester le pipeline sans dépendre d'un site externe.

### Inclus

* abstraction commune des sources ;
* `FakeJobSource` ou équivalent ;
* fixtures réalistes ;
* offres avec différents contrats, villes et compétences ;
* cas volontairement incomplets ;
* cas volontairement similaires pour préparer la déduplication ;
* snapshots bruts ;
* tests.

### Jeu de données fictif

Les fixtures doivent permettre de représenter notamment :

* offres classiques ;
* remote ;
* hybride ;
* différentes villes ;
* différents contrats ;
* salaire absent ;
* expérience absente ;
* technologies diverses ;
* offres potentiellement dupliquées.

### Explicitement non inclus

* connexion à un site externe ;
* scraping réel ;
* Playwright ;
* matching ;
* déduplication réelle.

### Critères de validation

* [ ] interface de source définie ;
* [ ] collecteur fictif fonctionnel ;
* [ ] fixtures déterministes ;
* [ ] données brutes produites ;
* [ ] tests sans dépendance réseau ;
* [ ] quality gate valide.

---

## Étape 8 — Pipeline collecte → normalisation → stockage

**État : ⬜ À FAIRE**

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
* création des snapshots ;
* persistence des offres ;
* gestion des erreurs partielles ;
* logs ;
* tests du pipeline complet.

### Normalisation initiale

Prévoir notamment :

* titres ;
* entreprises ;
* URLs ;
* localisations ;
* pays ;
* villes ;
* contrat ;
* remote ;
* dates ;
* salaires lorsque disponibles.

### Explicitement non inclus

* déduplication avancée ;
* scraping réel ;
* matching ;
* NLP.

### Critères de validation

* [ ] pipeline complet fonctionnel avec FakeJobSource ;
* [ ] snapshots conservés ;
* [ ] offres normalisées persistées ;
* [ ] erreurs d'une offre n'arrêtant pas nécessairement tout le batch ;
* [ ] tests d'intégration présents ;
* [ ] quality gate valide.

---

## Étape 9 — Déduplication

**État : ⬜ À FAIRE**

### Objectif

Identifier plusieurs occurrences représentant probablement la même offre sans perte de provenance.

### Stratégie

Déduplication progressive utilisant plusieurs niveaux :

1. identifiants forts ;
2. URL canonique ;
3. hash exact ;
4. fingerprint déterministe ;
5. similarité floue si nécessaire.

### Résultats possibles

* `NOT_DUPLICATE`
* `POSSIBLE_DUPLICATE`
* `CONFIRMED_DUPLICATE`

### Principe fondamental

Une occurrence source ne doit pas être supprimée lorsqu'elle correspond à une offre déjà connue.

Elle doit être reliée à l'offre canonique correspondante.

### Inclus

* fingerprints ;
* normalisation nécessaire à la comparaison ;
* stratégie de décision ;
* association des occurrences ;
* tests unitaires ;
* tests du pipeline.

### Explicitement non inclus

* embeddings ;
* similarité vectorielle ;
* LLM ;
* matching utilisateur.

### Critères de validation

* [ ] doublons exacts détectés ;
* [ ] provenance conservée ;
* [ ] cas ambigus non fusionnés agressivement ;
* [ ] tests de faux positifs et faux négatifs ;
* [ ] quality gate valide.

---

## Étape 10 — Premier connecteur réel

**État : ⬜ À FAIRE**

### Objectif

Brancher une seule source externe réelle sur le pipeline déjà validé.

### Avant toute implémentation

Créer ou mettre à jour une fiche source contenant :

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
2. flux structuré ;
3. HTTP + parsing ;
4. crawler spécialisé ;
5. navigateur automatisé uniquement si nécessaire et autorisé.

### Interdictions

Ne jamais contourner :

* CAPTCHA ;
* authentification ;
* paywalls ;
* protections anti-bot ;
* limitations explicitement destinées à empêcher l'automatisation.

### Inclus

* une seule source réelle ;
* intégration à l'abstraction existante ;
* gestion des timeouts ;
* gestion des erreurs réseau ;
* rate limiting raisonnable ;
* fixtures de tests ;
* tests ne dépendant pas directement du site réel.

### Critères de validation

* [ ] conformité de la méthode de collecte étudiée ;
* [ ] fiche source documentée ;
* [ ] connecteur isolé du cœur métier ;
* [ ] pipeline existant réutilisé ;
* [ ] tests à base de fixtures ;
* [ ] quality gate valide.

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

Prévoir des critères distincts du score, notamment :

* contrat obligatoire ;
* localisation incompatible ;
* durée incompatible ;
* disponibilité ;
* compétence obligatoire ;
* langue obligatoire.

### Gestion de l'incertitude

Utiliser explicitement :

* `MATCH`
* `MISMATCH`
* `UNKNOWN`

Une donnée absente dans l'offre ne doit pas automatiquement être considérée comme incompatible.

### Versionnement

Le résultat doit enregistrer la version du moteur, par exemple :

```text
deterministic-v1
```

### Explicabilité

Le résultat doit fournir :

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
* [ ] explication générée à partir du calcul réel ;
* [ ] version du moteur conservée ;
* [ ] tests unitaires approfondis ;
* [ ] quality gate valide.

---

# Phase E — Frontend MVP

## Étape 12 — Frontend : liste et détail des offres

**État : ⬜ À FAIRE**

### Objectif

Créer la première interface réellement utilisable de consultation des offres.

### Inclus

#### Liste

Afficher notamment :

* titre ;
* entreprise ;
* localisation ;
* contrat ;
* remote ;
* date ;
* score lorsqu'il existe ;
* compétences principales.

#### Fonctionnalités

* pagination ;
* recherche textuelle simple ;
* filtres ;
* tri ;
* navigation vers le détail.

#### Détail

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
* [ ] chargement API géré ;
* [ ] erreurs API gérées ;
* [ ] filtres essentiels ;
* [ ] détail fonctionnel ;
* [ ] tests frontend principaux.

---

## Étape 13 — Frontend : profil et préférences

**État : ⬜ À FAIRE**

### Objectif

Permettre à l'utilisateur de consulter et modifier son profil depuis l'interface.

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
* critères à éviter ;
* validation frontend ;
* synchronisation API.

### Explicitement non inclus

* import CV ;
* apprentissage automatique des préférences.

### Critères de validation

* [ ] lecture du profil ;
* [ ] modification ;
* [ ] sauvegarde ;
* [ ] validation ;
* [ ] erreurs API gérées ;
* [ ] tests frontend principaux.

---

## Étape 14 — Favoris, rejets et archivage

**État : ⬜ À FAIRE**

### Objectif

Permettre à l'utilisateur d'indiquer ses décisions sur les offres.

### Interactions initiales

* `view`
* `favorite`
* `reject`
* `archive`

### Inclus

* modèle d'interaction ;
* migration ;
* service ;
* endpoints API ;
* actions frontend ;
* filtres par statut ;
* tests.

### Explicitement non inclus

* apprentissage automatique du comportement ;
* ajustement automatique des préférences.

### Critères de validation

* [ ] favoris persistés ;
* [ ] rejets persistés ;
* [ ] archives persistées ;
* [ ] interface mise à jour ;
* [ ] tests backend et frontend.

---

## Étape 15 — Suivi des candidatures

**État : ⬜ À FAIRE**

### Objectif

Permettre le suivi complet des candidatures.

### Statuts initiaux

* `TO_REVIEW`
* `FAVORITE`
* `TO_PREPARE`
* `APPLIED`
* `INTERVIEW`
* `TECHNICAL_TEST`
* `OFFER_RECEIVED`
* `REJECTED`
* `WITHDRAWN`
* `ARCHIVED`

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

# 🎯 Frontière MVP

Les Étapes **0 à 15** constituent le chemin vers le MVP fonctionnel.

À l'issue de l'Étape 15, l'application doit être utilisable sans dépendre d'un LLM ou d'une recherche vectorielle.

Le MVP doit permettre le flux suivant :

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

Aucune fonctionnalité post-MVP ne doit être nécessaire au fonctionnement de ce flux.

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

Le CV complète le profil mais ne l'écrase jamais automatiquement.

---

## Étape 17 — Enrichissement NLP

**État : ⬜ POST-MVP**

### Objectif

Améliorer l'extraction structurée du contenu des annonces.

### Cibles

* compétences ;
* technologies ;
* missions ;
* langues ;
* niveau d'expérience ;
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

Ne pas introduire une base vectorielle séparée sans besoin démontré.

### Inclus

* extension pgvector ;
* stratégie d'embeddings ;
* abstraction `EmbeddingProvider` ;
* stockage des embeddings ;
* versionnement du modèle ;
* recalcul contrôlé.

---

## Étape 19 — Recherche sémantique

**État : ⬜ POST-MVP**

### Objectif

Permettre des recherches en langage naturel combinant plusieurs signaux.

### Exemple

> Je cherche un stage en machine learning à Paris avec Python et idéalement du NLP.

### Approche cible

Combiner :

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

Le système peut seulement proposer des changements nécessitant confirmation.

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
* autres intégrations ultérieurement.

### Contraintes

* seuil configurable ;
* pas de notifications dupliquées ;
* alertes désactivables.

---

## Étape 23 — Stabilisation, optimisation et documentation finale

**État : ⬜ POST-MVP**

### Objectif

Stabiliser l'ensemble du système après validation fonctionnelle.

### Axes

* tests ;
* couverture des cas limites ;
* performance ;
* index PostgreSQL ;
* sécurité ;
* logs ;
* gestion des erreurs ;
* UX ;
* documentation ;
* nettoyage architectural ;
* suppression des abstractions devenues inutiles ;
* vérification des dépendances ;
* revue de confidentialité.

---

# Quality gate général

Pour toute étape backend, exécuter lorsque pertinent :

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

Une étape n'est pas considérée comme terminée si les contrôles applicables échouent, sauf limitation explicitement documentée et acceptée.

Pour les étapes frontend, exécuter également les contrôles TypeScript, lint et tests configurés dans le projet.

Ne jamais déclarer une commande comme réussie si elle n'a pas réellement été exécutée.

---

# Règles de progression

Avant de commencer une étape :

1. lire `.github/copilot-instructions.md` ;
2. lire `docs/PROJECT_SPEC.md` ;
3. lire `docs/ARCHITECTURE.md` ;
4. lire cette roadmap ;
5. inspecter l'état réel du repository.

Pendant une étape :

1. respecter strictement son périmètre ;
2. éviter les fonctionnalités futures ;
3. ajouter les tests correspondants ;
4. maintenir le typage ;
5. documenter les décisions structurantes.

À la fin d'une étape :

1. exécuter les quality gates applicables ;
2. corriger les erreurs appartenant au périmètre ;
3. mettre à jour cette roadmap ;
4. documenter les limitations restantes ;
5. effectuer une revue des changements ;
6. créer un commit Git cohérent.

Une étape suivante ne doit jamais être commencée automatiquement.

---

# État actuel

```text
Étape 0  ✅ Architecture
Étape 1  ✅ Bootstrap
Étape 2  ✅ Infrastructure locale
Étape 3  ✅ Persistence
Étape 4  ✅ Fondation FastAPI
────────────────────────────────────
Étape 5  ⬜ Profil utilisateur       ← PROCHAINE ÉTAPE
Étape 6  ⬜ Domaine/API offres
Étape 7  ⬜ Collecteur fictif
Étape 8  ⬜ Pipeline
Étape 9  ⬜ Déduplication
Étape 10 ⬜ Première source réelle
Étape 11 ⬜ Matching V1
Étape 12 ⬜ Frontend offres
Étape 13 ⬜ Frontend profil
Étape 14 ⬜ Interactions
Étape 15 ⬜ Candidatures
────────────────────────────────────
            MVP
────────────────────────────────────
Étape 16 ⬜ CV
Étape 17 ⬜ NLP
Étape 18 ⬜ Embeddings / pgvector
Étape 19 ⬜ Recherche sémantique
Étape 20 ⬜ Matching hybride
Étape 21 ⬜ Scheduler
Étape 22 ⬜ Alertes
Étape 23 ⬜ Stabilisation
```

**Prochaine étape autorisée : Étape 5 — Profil utilisateur et préférences.**
