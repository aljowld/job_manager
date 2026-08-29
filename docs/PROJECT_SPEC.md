# Job Finder — Project Specification

## Statut

Ce document constitue la **spécification produit de référence** du projet Job Finder.

Il définit :

* la vision du produit ;
* les objectifs fonctionnels ;
* les contraintes fondamentales ;
* les règles métier importantes ;
* les exigences de collecte ;
* les exigences de matching ;
* les exigences de confidentialité et de sécurité ;
* les principes techniques qui ne doivent pas être remis en cause sans décision explicite.

Il ne doit pas dupliquer inutilement les documents opérationnels du repository.

Les sources de vérité sont réparties ainsi :

| Document                          | Responsabilité                                                |
| --------------------------------- | ------------------------------------------------------------- |
| `docs/PROJECT_SPEC.md`            | Ce que le produit doit faire et ses contraintes fondamentales |
| `docs/ARCHITECTURE.md`            | Architecture réellement adoptée                               |
| `docs/ROADMAP.md`                 | Ordre, périmètre et état des étapes                           |
| `docs/DEVELOPMENT.md`             | Commandes et workflow de développement                        |
| `.github/copilot-instructions.md` | Règles permanentes pour GitHub Copilot                        |
| `docs/adr/`                       | Décisions architecturales structurantes                       |

En cas de divergence :

1. la spécification produit reste la référence pour les besoins fonctionnels ;
2. `ARCHITECTURE.md` représente l'architecture effectivement adoptée ;
3. `ROADMAP.md` représente l'ordre de développement effectivement retenu ;
4. toute modification d'une décision structurante doit être documentée.

---

# 1. Vision du produit

Le projet ne consiste pas à construire un simple scraper.

L'objectif est de construire un **assistant personnel intelligent de recherche de stages et d'emplois** capable de répondre à la question :

> Parmi toutes les offres disponibles, lesquelles sont réellement intéressantes pour moi, et pourquoi ?

L'application doit progressivement permettre de :

1. récupérer des offres depuis plusieurs sources autorisées ;
2. conserver les données originales ;
3. normaliser les offres dans un modèle commun ;
4. détecter les doublons ;
5. conserver la provenance de chaque offre ;
6. structurer les informations importantes des annonces ;
7. gérer un profil utilisateur détaillé ;
8. gérer des préférences et contraintes ;
9. comparer une offre au profil ;
10. appliquer des critères éliminatoires ;
11. calculer un score de compatibilité ;
12. expliquer ce score ;
13. classer les offres ;
14. rechercher et filtrer les offres ;
15. sauvegarder, rejeter ou archiver des offres ;
16. suivre les candidatures ;
17. enregistrer les interactions ;
18. importer ultérieurement un CV ;
19. ajouter ultérieurement des capacités NLP ;
20. ajouter ultérieurement une recherche sémantique ;
21. apprendre progressivement des préférences observées ;
22. automatiser progressivement la collecte ;
23. envoyer éventuellement des alertes.

L'application est initialement destinée à un **usage personnel**.

---

# 2. Priorités du projet

Les décisions doivent privilégier, dans cet ordre :

1. fiabilité ;
2. simplicité ;
3. maintenabilité ;
4. confidentialité ;
5. pertinence des recommandations ;
6. testabilité ;
7. performance ;
8. fonctionnalités avancées.

Une solution plus complexe ne doit être adoptée que si elle apporte un bénéfice concret et démontré.

Principe directeur :

> Construire la solution la plus simple capable de répondre correctement au besoin actuel.

---

# 3. Périmètre du MVP

Le MVP doit fournir une application réellement utilisable **sans nécessiter de LLM, d'embeddings ou de machine learning**.

## Inclus dans le MVP

Le MVP doit permettre :

* de renseigner un profil utilisateur ;
* de définir des préférences ;
* de collecter au moins une source réelle autorisée ;
* de conserver les données brutes ;
* de normaliser les offres ;
* de détecter les doublons ;
* de conserver plusieurs occurrences d'une même offre ;
* de calculer un matching déterministe ;
* d'expliquer le score ;
* de consulter les offres dans une interface ;
* de rechercher et filtrer ;
* de mettre une offre en favori ;
* de rejeter une offre ;
* d'archiver une offre ;
* de suivre une candidature ;
* de lancer l'application localement avec PostgreSQL ;
* de disposer de tests et d'une documentation suffisante.

## Hors MVP

Ne sont pas nécessaires pour valider le MVP :

* LLM ;
* embeddings ;
* pgvector ;
* recherche sémantique ;
* machine learning ;
* analyse automatique de CV ;
* personnalisation comportementale avancée ;
* Redis ;
* Celery ;
* architecture distribuée ;
* microservices ;
* alertes automatisées ;
* mobile ;
* extension navigateur ;
* génération automatique de CV ;
* génération automatique de lettres de motivation.

La frontière détaillée et l'ordre exact des étapes sont définis dans :

`docs/ROADMAP.md`

---

# 4. Architecture générale imposée

Le projet doit commencer et rester, pour le MVP, un **monolithe modulaire**.

Il doit comprendre principalement :

* un backend Python / FastAPI ;
* PostgreSQL ;
* SQLAlchemy 2 ;
* Alembic ;
* Pydantic v2 ;
* un frontend React + TypeScript + Vite.

L'architecture détaillée effectivement retenue est documentée dans :

`docs/ARCHITECTURE.md`

Ne pas introduire sans besoin concret :

* microservices ;
* Redis ;
* Celery ;
* Kafka ;
* Elasticsearch ;
* MongoDB ;
* Kubernetes ;
* base vectorielle externe.

PostgreSQL doit rester la source de vérité principale.

---

# 5. Organisation actuelle du repository

L'organisation générale actuelle est :

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
│
├── docs/
└── .github/
```

Les chemins détaillés et leur rôle sont documentés dans :

* `docs/ARCHITECTURE.md`
* `docs/DEVELOPMENT.md`

Ne pas recréer les anciens dossiers racine :

```text
backend/
frontend/
```

Le backend se trouve sous :

```text
src/backend/
```

Le frontend se trouve sous :

```text
src/frontend/
```

---

# 6. Toolchain Python

Le projet Python utilise obligatoirement les outils Astral suivants :

* `uv`
* Ruff
* ty

ainsi que :

* pytest.

Les fichiers du projet Python sont situés à la racine :

```text
pyproject.toml
uv.lock
```

---

# 7. uv

`uv` est le gestionnaire principal pour :

* le projet Python ;
* les dépendances ;
* l'environnement ;
* le lockfile ;
* l'exécution des outils Python.

Ne pas créer un second workflow basé sur :

```text
requirements.txt
pip install -r ...
```

sans décision explicite.

Les dépendances Python doivent être ajoutées avec `uv`.

Exemple :

```bash
uv add <dependency>
```

`uv.lock` doit être versionné.

Ne jamais modifier `uv.lock` manuellement.

---

# 8. Ruff

Ruff est responsable :

* du linting ;
* du formatage ;

du **code applicatif backend**.

Le périmètre principal est :

```text
src/backend/app/
```

Les tests backend sont volontairement exclus de Ruff.

Cette décision est intentionnelle : les tests doivent prioritairement être jugés sur leur comportement et non sur le coût de maintenance du linting de mocks, fixtures ou helpers de tests.

---

# 9. ty

ty est le vérificateur statique de types du **code applicatif backend**.

Le périmètre principal est :

```text
src/backend/app/
```

Les tests backend :

```text
src/backend/tests/
```

sont volontairement exclus de ty.

Le code applicatif doit rester correctement typé.

Éviter :

* les `Any` inutiles ;
* les suppressions globales d'erreurs ;
* les annotations imprécises sans justification.

---

# 10. pytest

pytest est responsable de la validation des tests backend.

Les tests sont situés dans :

```text
src/backend/tests/
```

Ils doivent principalement vérifier :

* comportement ;
* régressions ;
* intégrité des données ;
* contrats API ;
* règles métier ;
* fonctionnement des pipelines.

---

# 11. Quality gate backend

Le quality gate est exécuté depuis la racine du repository :

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest src/backend/tests
```

Répartition :

```text
src/backend/app/     → Ruff + Ruff format + ty
src/backend/tests/   → pytest
```

Une nouvelle étape ne doit pas introduire de nouvelles erreurs dans ces contrôles.

Les erreurs réellement préexistantes et indépendantes doivent être identifiées comme telles et documentées.

---

# 12. Backend

Le backend utilise :

* Python ;
* FastAPI ;
* Pydantic v2 ;
* Pydantic Settings ;
* SQLAlchemy 2 ;
* Alembic ;
* PostgreSQL.

HTTPX est privilégié pour les appels HTTP lorsque pertinent.

BeautifulSoup peut être utilisé pour du parsing HTML simple.

Playwright ne doit être utilisé que lorsqu'une solution HTTP classique est insuffisante et lorsque l'automatisation est appropriée.

---

# 13. Architecture backend

La séparation doit rester pragmatique.

Architecture conceptuelle :

```text
API
 ↓
Application / Services
 ↓
Domain / Business rules
 ↓
Persistence / External adapters
```

Les routes FastAPI doivent rester légères.

Éviter :

* logique métier complexe dans les routes ;
* SQL dispersé dans les endpoints ;
* dépendances FastAPI dans le cœur métier ;
* architecture Clean/Hexagonale excessivement cérémonielle ;
* multiplication de couches sans valeur réelle.

Un service ou repository doit exister uniquement s'il clarifie réellement une responsabilité.

---

# 14. Frontend

Le frontend utilise :

* React ;
* TypeScript ;
* Vite.

TypeScript doit rester en mode strict.

Ne pas introduire Next.js sans besoin réel.

Le frontend doit progressivement être organisé par fonctionnalités.

Exemples :

```text
features/
├── jobs/
├── profile/
├── applications/
└── recommendations/
```

Ne pas introduire un gestionnaire d'état global lourd sans besoin concret.

Une bibliothèque spécialisée pour les données serveur, telle que TanStack Query, peut être utilisée lorsqu'elle apporte une valeur claire.

---

# 15. PostgreSQL

PostgreSQL est la source de vérité du système.

Il doit stocker notamment :

* offres ;
* occurrences sources ;
* snapshots bruts ;
* profil ;
* préférences ;
* interactions ;
* candidatures ;
* résultats de matching lorsque pertinent.

Ne pas ajouter une nouvelle base uniquement parce qu'une fonctionnalité pourrait éventuellement en bénéficier.

Pour la recherche sémantique future, privilégier d'abord :

```text
PostgreSQL + pgvector
```

---

# 16. Modèle JobSource

Une source représente un fournisseur d'offres.

Informations conceptuelles possibles :

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

La modélisation réellement implémentée peut évoluer par migration.

---

# 17. RawJobSnapshot

Les données récupérées doivent être conservées autant que possible avant transformation.

Conceptuellement :

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

Objectif :

> pouvoir rejouer parsing, normalisation ou enrichissement sans devoir systématiquement recontacter la source.

---

# 18. JobOffer

`JobOffer` représente une offre canonique.

Champs potentiels :

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

Le modèle doit rester évolutif.

Ne pas ajouter toutes les données futures dans une seule table uniquement pour anticiper des fonctionnalités non développées.

---

# 19. Provenance des offres

Une même offre peut apparaître sur plusieurs sources.

Le système doit conserver les différentes occurrences.

Modèle conceptuel :

```text
JobOffer
   │
   ├── occurrence source A
   ├── occurrence source B
   └── occurrence source C
```

Une occurrence peut conserver notamment :

```text
source
external_job_id
source_url
raw_snapshot
collected_at
```

La provenance ne doit pas être perdue lors de la déduplication.

---

# 20. Profil utilisateur

Le profil utilisateur constitue la source structurée utilisée par le matching.

Il doit progressivement permettre de représenter :

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
* rôles recherchés ;
* rôles exclus ;
* salaire souhaité ;
* disponibilité ;
* durée de stage ;
* entreprises préférées ;
* entreprises exclues.

L'application est initialement mono-utilisateur.

Il n'est pas nécessaire de créer un système complet de comptes utilisateurs pour le MVP.

---

# 21. Préférences

Les préférences doivent pouvoir représenter différents degrés d'importance.

Valeurs conceptuelles :

```text
REQUIRED
VERY_IMPORTANT
IMPORTANT
BONUS
AVOID
EXCLUDED
```

Le système doit distinguer :

* une préférence ;
* un critère obligatoire ;
* une exclusion.

Exemple :

```text
Python → VERY_IMPORTANT
Stage → REQUIRED
Commercial → EXCLUDED
```

Le moteur de matching doit pouvoir exploiter ultérieurement ces différences.

---

# 22. CV

L'import de CV est une fonctionnalité post-MVP.

Formats prévus :

* PDF ;
* DOCX.

Informations potentiellement extraites :

* expériences ;
* formations ;
* compétences ;
* technologies ;
* langues ;
* projets ;
* certifications ;
* intitulés de postes.

Pipeline conceptuel :

```text
CV
 ↓
extraction texte
 ↓
extraction structurée
 ↓
proposition de données
 ↓
validation utilisateur
 ↓
profil
```

Le CV ne doit jamais écraser automatiquement le profil utilisateur.

Toute donnée extraite doit pouvoir être :

* vérifiée ;
* modifiée ;
* rejetée.

---

# 23. Architecture de collecte

Les sources doivent respecter une abstraction commune.

Le collecteur doit essentiellement transformer :

```text
source externe
      ↓
données brutes identifiées
```

et non exécuter toute la logique métier.

Pipeline global :

```text
Source
  ↓
Collecte
  ↓
RawJobSnapshot
  ↓
Parsing
  ↓
Normalisation
  ↓
JobOfferCandidate
  ↓
Déduplication
  ↓
JobOffer canonique
  ↓
Matching
```

Les composants doivent rester séparables et testables.

---

# 24. Politique concernant les sources

Avant d'implémenter une source réelle :

1. rechercher une API officielle ;
2. rechercher un flux RSS/XML/JSON ;
3. vérifier les conditions applicables ;
4. examiner `robots.txt` lorsque pertinent ;
5. vérifier les restrictions d'accès ;
6. vérifier la nécessité d'une authentification ;
7. déterminer une fréquence raisonnable ;
8. documenter la stratégie retenue.

Pour chaque source réelle, documenter au minimum :

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

---

# 25. Interdictions concernant la collecte

Ne jamais contourner :

* CAPTCHA ;
* authentification ;
* paywalls ;
* protections anti-bot ;
* rate limits ;
* restrictions techniques destinées à empêcher l'automatisation.

Ne pas proposer de mécanisme visant à :

* masquer volontairement un bot ;
* contourner une protection ;
* contourner une restriction d'accès.

Si une source n'est pas raisonnablement automatisable, proposer :

* API ;
* feed ;
* export ;
* import manuel ;
* autre source.

---

# 26. Méthode de collecte

Toujours choisir la méthode la plus simple appropriée.

Ordre de préférence :

```text
API officielle
     ↓
feed structuré
     ↓
HTTP + parsing
     ↓
crawler spécialisé
     ↓
navigateur automatisé
```

Ne pas utiliser Playwright par défaut.

Un collecteur doit gérer raisonnablement :

* timeouts ;
* erreurs réseau ;
* réponses invalides ;
* rate limiting ;
* retries ;
* changements de structure ;
* erreurs partielles ;
* logging.

La panne d'une source ne doit pas provoquer l'échec de tout le système.

---

# 27. Normalisation

Les différentes sources doivent produire un modèle commun.

Pipeline :

```text
RawJob
   ↓
validation
   ↓
parsing
   ↓
normalisation
   ↓
JobOfferCandidate
```

Normaliser progressivement :

* titres ;
* entreprises ;
* URLs ;
* pays ;
* villes ;
* contrat ;
* remote/hybrid/on-site ;
* monnaies ;
* salaires ;
* dates ;
* technologies ;
* compétences ;
* niveaux d'expérience.

Ne pas perdre inutilement les valeurs originales.

Lorsque nécessaire, conserver simultanément :

```text
raw value
normalized value
```

---

# 28. Déduplication

La déduplication doit être :

* progressive ;
* explicable ;
* conservatrice ;
* non destructive.

## Niveau 1 — Identifiants forts

Exemples :

```text
source + external_job_id
canonical URL
content hash
```

## Niveau 2 — Fingerprint

Exemple :

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

* titres ;
* descriptions ;
* dates ;
* localisations.

## Niveau 4 — Similarité sémantique

Uniquement plus tard, si les étapes précédentes sont insuffisantes.

Résultats possibles :

```text
NOT_DUPLICATE
POSSIBLE_DUPLICATE
CONFIRMED_DUPLICATE
```

Un doublon confirmé doit être relié à une offre canonique.

Il ne doit pas être simplement supprimé.

---

# 29. Matching V1

Le premier moteur doit être **entièrement déterministe**.

Ne pas commencer par un LLM.

Composantes possibles :

```text
skills
technologies
location
contract
education
experience
languages
industry
remote
salary
duration
role
```

Calcul conceptuel :

```text
final_score =
    somme(component_score × component_weight)
```

Les pondérations doivent être configurables.

---

# 30. Critères éliminatoires

Les contraintes bloquantes sont distinctes du score.

Exemple :

```text
Recherche :
stage obligatoire

Offre :
CDI

Résultat :
eligible = false
```

Critères possibles :

* contrat ;
* localisation ;
* mobilité ;
* durée ;
* disponibilité ;
* diplôme ;
* compétence obligatoire ;
* langue obligatoire ;
* rôle exclu.

---

# 31. Gestion de l'incertitude

Le moteur doit distinguer :

```text
MATCH
MISMATCH
UNKNOWN
```

Une information absente n'est pas une incompatibilité.

Exemple :

```text
Profil :
salaire souhaité = 1500 €

Offre :
salaire absent
```

Résultat :

```text
UNKNOWN
```

et non :

```text
MISMATCH
```

---

# 32. Explicabilité

Le score doit être explicable.

Exemple :

```text
Compatibilité : 87 %

Critères obligatoires
✓ Stage
✓ Localisation compatible

Points forts
✓ Python
✓ SQL
✓ Machine Learning

Points faibles
⚠ AWS demandé mais absent du profil

Informations inconnues
? Salaire non indiqué
```

L'explication doit provenir des éléments réellement utilisés par le moteur.

Un LLM ne doit pas inventer une justification indépendante du calcul.

---

# 33. Versionnement du matching

Chaque version du moteur doit être identifiable.

Exemples :

```text
deterministic-v1
deterministic-v2
hybrid-v1
```

Le résultat doit pouvoir conserver la version utilisée.

Objectifs :

* reproductibilité ;
* comparaison ;
* recalcul ;
* compréhension des changements de classement.

---

# 34. Recherche et filtres

L'application doit permettre progressivement de filtrer les offres selon notamment :

* date ;
* localisation ;
* distance ;
* remote ;
* contrat ;
* durée ;
* entreprise ;
* industrie ;
* catégorie ;
* compétences ;
* technologies ;
* expérience ;
* formation ;
* score ;
* statut utilisateur.

Les filtres compatibles avec la pagination doivent être appliqués côté backend.

---

# 35. API

L'API est versionnée sous :

```text
/api/v1
```

Endpoints principaux prévus :

```text
GET    /api/v1/jobs
GET    /api/v1/jobs/{id}

GET    /api/v1/profile
PUT    /api/v1/profile

POST   /api/v1/jobs/{id}/favorite
POST   /api/v1/jobs/{id}/reject
POST   /api/v1/jobs/{id}/archive

GET    /api/v1/applications
POST   /api/v1/applications
GET    /api/v1/applications/{id}
PATCH  /api/v1/applications/{id}
```

Endpoints post-MVP possibles :

```text
POST   /api/v1/cv
GET    /api/v1/recommendations
GET    /api/v1/search
```

L'API doit utiliser :

* Pydantic v2 ;
* validation explicite ;
* pagination ;
* filtres ;
* codes HTTP corrects ;
* gestion centralisée des erreurs ;
* OpenAPI.

---

# 36. Repository pattern

Ne pas disperser des requêtes SQL complexes dans les routes API.

Utiliser des repositories lorsque cela clarifie la persistence d'un domaine.

Exemples :

* jobs ;
* profile ;
* applications ;
* interactions.

Éviter les abstractions excessivement génériques telles que :

```text
GenericRepository[T]
```

si elles rendent le code moins clair.

---

# 37. Transactions

Les opérations importantes doivent être transactionnellement cohérentes.

Exemple :

```text
collect
→ save raw snapshot
→ normalize
→ create/update canonical job
→ create source occurrence
```

Une erreur intermédiaire ne doit pas laisser un état partiellement écrit.

Même principe pour le profil et ses relations.

---

# 38. Interactions utilisateur

Les interactions à enregistrer progressivement sont :

```text
view
favorite
reject
apply
archive
```

Elles permettront plus tard d'analyser des tendances.

Le système peut éventuellement proposer :

> Tu sauvegardes régulièrement des offres NLP. Souhaites-tu augmenter l'importance de cette préférence ?

Mais il ne doit **jamais modifier automatiquement une préférence critique sans confirmation explicite**.

---

# 39. Candidatures

Le système doit permettre de suivre les candidatures.

Statuts possibles :

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

Une candidature peut contenir :

```text
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

# 40. Frontend métier

## Liste des offres

Afficher progressivement :

```text
titre
entreprise
localisation
remote
contrat
date
score
compétences principales
source(s)
```

Permettre :

* recherche ;
* filtres ;
* tri ;
* détail ;
* favori ;
* rejet ;
* archivage.

## Détail

Afficher notamment :

* description ;
* informations structurées ;
* provenance ;
* compétences ;
* technologies ;
* score ;
* composantes du score ;
* critères bloquants ;
* points forts ;
* points faibles ;
* informations inconnues ;
* lien original.

## Profil

Permettre de consulter et modifier les informations du profil et les préférences.

## Candidatures

Permettre de consulter et mettre à jour les candidatures.

---

# 41. IA et NLP

Les fonctionnalités IA arrivent **après le MVP déterministe**.

Utiliser d'abord :

* règles ;
* parsing ;
* normalisation ;
* méthodes locales ;
* NLP classique ;

lorsque cela suffit.

Objectifs futurs :

* extraction de compétences ;
* technologies ;
* missions ;
* niveaux ;
* langues ;
* informations implicites ;
* embeddings ;
* comparaison sémantique.

---

# 42. Abstraction IA future

Ne pas lier le domaine à un fournisseur IA spécifique.

Lorsque la roadmap atteint cette phase, des abstractions telles que :

```text
EmbeddingProvider
LLMProvider
JobInformationExtractor
```

pourront être introduites.

Ne pas les créer prématurément.

Lorsqu'une IA externe est utilisée, conserver lorsque pertinent :

```text
provider
model
model_version
prompt_version
created_at
```

---

# 43. Recherche sémantique

Fonctionnalité post-MVP.

Exemple :

> Je cherche un stage en machine learning à Paris avec Python et idéalement du NLP.

Approche prévue :

```text
filtres structurés
+
recherche textuelle
+
similarité vectorielle
```

Privilégier :

```text
PostgreSQL + pgvector
```

avant d'introduire une nouvelle base spécialisée.

---

# 44. Scheduler

La collecte doit d'abord fonctionner :

* manuellement ;
* de manière testable ;
* avec une commande claire.

L'automatisation arrivera plus tard.

Architecture conceptuelle :

```text
Scheduler
   ↓
Collection
   ↓
Normalization
   ↓
Deduplication
   ↓
Enrichment
   ↓
Matching
   ↓
Alerts
```

Ne pas introduire Celery + Redis uniquement pour disposer d'un scheduler.

---

# 45. Alertes

Les alertes sont post-MVP.

Exemple :

```text
Nouvelle offre correspondant à 92 % de ton profil.
```

Canaux futurs possibles :

* application ;
* email ;
* autres intégrations.

Elles doivent être :

* configurables ;
* désactivables ;
* non dupliquées inutilement.

---

# 46. Observabilité

Utiliser des logs structurés.

Exemples :

```text
collection.started
source.collection.started
source.collection.completed
jobs.collected
jobs.created
duplicates.detected
matching.completed
source.unavailable
```

Une collecte pourra disposer d'un identifiant tel que :

```text
collection_run_id
```

Statistiques utiles :

* offres trouvées ;
* nouvelles offres ;
* offres mises à jour ;
* doublons ;
* erreurs ;
* durée ;
* annonces analysées ;
* recommandations élevées.

Ne pas introduire une stack d'observabilité complexe pour le MVP.

---

# 47. Gestion des erreurs

Les erreurs doivent être explicites.

Exemples futurs :

```text
SourceUnavailableError
SourceRateLimitedError
JobParsingError
JobNormalizationError
InvalidJobDataError
InvalidCVError
MatchingError
AIServiceError
```

Ne pas utiliser d'`except Exception` silencieux.

À la frontière HTTP :

```text
Application/domain error
        ↓
FastAPI exception handler
        ↓
HTTP response
```

Ne pas exposer :

* stack traces ;
* secrets ;
* détails internes inutiles.

---

# 48. Configuration

Centraliser la configuration.

Utiliser :

```text
.env
.env.example
Pydantic Settings
```

Variables potentielles :

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
EMBEDDING_PROVIDER
EMBEDDING_MODEL
```

Ajouter uniquement les variables nécessaires à l'étape réellement implémentée.

Ne jamais versionner les secrets.

---

# 49. Sécurité

Même pour une application personnelle :

* valider les entrées ;
* protéger les secrets ;
* contrôler les futurs uploads ;
* limiter les tailles de fichiers ;
* vérifier les types de fichiers ;
* éviter les chemins arbitraires ;
* utiliser correctement SQLAlchemy ;
* ne jamais logger de secrets ;
* ne pas envoyer inutilement des données personnelles à des services externes.

Une authentification complète peut rester hors MVP tant que l'application reste strictement locale.

Avant toute exposition réseau non locale, la sécurité d'accès devra être réévaluée.

---

# 50. Confidentialité

Considérer comme sensibles :

* profil ;
* identité ;
* coordonnées ;
* expériences ;
* CV ;
* candidatures ;
* interactions.

Avant un appel à une IA externe :

1. identifier les données réellement nécessaires ;
2. minimiser les informations envoyées ;
3. éviter les données personnelles inutiles ;
4. documenter ce qui est envoyé ;
5. rendre le fournisseur configurable lorsque pertinent.

Les modèles locaux doivent rester une possibilité.

---

# 51. Tests backend

Les tests backend utilisent pytest.

Ils sont situés sous :

```text
src/backend/tests/
```

Prévoir progressivement des tests unitaires pour :

* parsing ;
* normalisation ;
* validation ;
* déduplication ;
* matching ;
* critères éliminatoires ;
* calcul des scores ;
* gestion de `UNKNOWN` ;
* services métier.

Tests d'intégration pour :

* PostgreSQL ;
* repositories ;
* FastAPI ;
* migrations ;
* transactions ;
* pipeline de collecte.

Les tests sont volontairement exclus de Ruff et ty.

---

# 52. Tests des collecteurs

Les collecteurs doivent être testés avec :

* fixtures HTML ;
* JSON ;
* XML ;
* payloads enregistrés ;
* mocks HTTP.

Les tests automatisés ne doivent pas dépendre du fonctionnement d'un site externe réel.

Exemple d'organisation future :

```text
src/backend/tests/fixtures/sources/
└── source_a/
    ├── listing.html
    ├── detail.html
    └── expected.json
```

---

# 53. Tests frontend

Prévoir progressivement :

* composants importants ;
* filtres ;
* formulaires ;
* interactions ;
* chargement API ;
* erreurs API.

Utiliser des données fictives ou une API mockée lorsque pertinent.

Les parcours complets critiques pourront ultérieurement disposer de tests end-to-end.

---

# 54. Docker

L'environnement local MVP comprend :

```text
docker-compose.yml
├── postgres
├── backend
└── frontend
```

Ne pas ajouter sans besoin :

```text
worker
redis
queue
```

Le build Python doit utiliser :

```text
pyproject.toml
uv.lock
```

situés à la racine du repository.

Les Dockerfiles doivent tenir compte de la structure actuelle :

```text
src/backend/
src/frontend/
```

---

# 55. Qualité du code

Le code applicatif doit être :

* lisible ;
* typé ;
* modulaire ;
* testable ;
* maintenable ;
* correctement nommé.

Éviter :

* fichiers gigantesques ;
* fonctions de centaines de lignes ;
* logique métier dans les routes ;
* abstraction prématurée ;
* classes purement cérémonielles ;
* duplication ;
* dépendances inutiles ;
* état global incontrôlé ;
* `Any` systématique ;
* commentaires qui répètent simplement le code.

SOLID peut être utilisé lorsqu'il améliore réellement la conception.

Ne pas appliquer un design pattern uniquement pour respecter une théorie architecturale.

---

# 56. Dépendances

Avant d'ajouter une dépendance :

1. déterminer si elle est nécessaire ;
2. vérifier si la bibliothèque standard suffit ;
3. vérifier si une dépendance existante couvre déjà le besoin ;
4. éviter les outils redondants ;
5. documenter les dépendances structurantes.

Les dépendances Python doivent être ajoutées avec uv.

Ne jamais modifier `uv.lock` manuellement.

---

# 57. Documentation

Maintenir au minimum :

```text
README.md
docs/PROJECT_SPEC.md
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DEVELOPMENT.md
```

Les décisions importantes peuvent être documentées sous :

```text
docs/adr/
```

Un ADR doit correspondre à une vraie décision structurante.

Ne pas créer un ADR pour un détail d'implémentation ordinaire.

---

# 58. Méthode de développement

Le projet doit être développé **étape par étape**.

L'ordre exact, le périmètre et le statut des étapes sont définis exclusivement dans :

```text
docs/ROADMAP.md
```

Ne pas dupliquer ici la roadmap détaillée afin d'éviter les divergences.

Pour chaque étape :

1. lire la documentation ;
2. inspecter le repository ;
3. comprendre le périmètre ;
4. implémenter uniquement l'étape demandée ;
5. ajouter les tests correspondants ;
6. exécuter les validations ;
7. corriger les régressions introduites ;
8. mettre à jour la documentation nécessaire ;
9. mettre à jour `ROADMAP.md` ;
10. arrêter avant l'étape suivante.

---

# 59. Definition of Done

Une fonctionnalité backend est considérée comme correctement implémentée lorsque :

```text
code applicatif
+
tests correspondants
+
Ruff sur le code applicatif
+
Ruff format sur le code applicatif
+
ty sur le code applicatif
+
pytest sur les tests
+
documentation pertinente
```

sont cohérents.

Quality gate :

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest src/backend/tests
```

Les tests backend sont volontairement exclus de Ruff et ty.

Une fonctionnalité ne doit pas être déclarée terminée si elle contient seulement du pseudo-code ou des placeholders représentant la fonctionnalité annoncée.

---

# 60. Gestion des erreurs de quality gate

Lorsqu'un contrôle échoue, distinguer :

1. erreur introduite ou affectée par l'étape courante ;
2. erreur préexistante réellement indépendante ;
3. origine incertaine.

Toute erreur introduite par le travail courant doit être corrigée.

Une erreur ne doit pas être qualifiée d'« hors périmètre » simplement parce qu'elle se trouve dans un fichier différent.

Les limitations réellement indépendantes peuvent être documentées sans bloquer systématiquement la progression si elles sont explicitement acceptées.

---

# 61. Discipline de scope

Ne pas implémenter plusieurs grandes étapes simultanément.

Ne pas anticiper :

* embeddings ;
* NLP ;
* scheduler ;
* alertes ;
* CV ;
* recherche sémantique ;
* nouvelles infrastructures ;

avant leur étape dédiée.

Lorsque la roadmap indique :

```text
Étape N
```

n'implémenter que cette étape et les modifications minimales nécessaires à son fonctionnement.

Ne pas réorganiser silencieusement la roadmap.

---

# 62. Fonctionnalités futures

L'architecture doit pouvoir évoluer vers :

* nouvelles sources ;
* nouveaux moteurs de matching ;
* NLP ;
* embeddings ;
* fournisseurs IA ;
* modèles locaux ;
* notifications ;
* statistiques ;
* extension navigateur ;
* mobile ;
* génération de CV ;
* génération de lettres ;
* personnalisation comportementale.

Mais :

> la possibilité d'une fonctionnalité future n'est pas une raison suffisante pour construire dès aujourd'hui son infrastructure.

Des frontières propres suffisent.

---

# 63. Ce qu'il ne faut pas faire

Éviter explicitement :

```text
microservices dès le MVP

Redis sans besoin concret

Celery sans besoin concret

Elasticsearch dès le MVP

base vectorielle externe dès le MVP

LLM pour chaque annonce

scraping Playwright systématique

scraper contenant toute la logique métier

logique métier dans les routes FastAPI

suppression destructive des doublons

matching opaque

données absentes automatiquement considérées négatives

modification silencieuse des préférences utilisateur

secrets dans Git

tests dépendant de sites externes

pip + uv utilisés comme workflows concurrents

multiplication de linters Python redondants

abstractions anticipant des fonctionnalités non encore développées

réorganisation silencieuse de la roadmap
```

---

# 64. Hiérarchie des décisions

Avant toute décision importante, vérifier dans cet ordre :

```text
PROJECT_SPEC
      ↓
ARCHITECTURE
      ↓
ROADMAP
      ↓
DEVELOPMENT
      ↓
implementation
```

Interprétation :

* `PROJECT_SPEC` définit le besoin ;
* `ARCHITECTURE` définit la manière adoptée de le construire ;
* `ROADMAP` définit quand le construire ;
* `DEVELOPMENT` définit comment travailler avec le repository.

---

# 65. Principe directeur final

À chaque décision, poser la question :

> Cette décision améliore-t-elle réellement notre capacité à identifier de manière fiable, compréhensible et maintenable les offres les plus pertinentes pour l'utilisateur ?

Si la réponse est non, simplifier.

Préférer :

```text
simple > complexe
explicite > implicite
déterministe > opaque
testé > supposé
progressif > massif
réversible > destructif
maintenable > ingénieux
```

Construire d'abord une excellente application déterministe et fiable.

Ajouter ensuite progressivement l'intelligence sémantique.

La complexité doit être justifiée par un besoin réel, jamais par anticipation.
