# Roadmap du projet

Statut actuel : Étape 2 — Infrastructure locale configurée, validation Docker bloquée par l’absence de Docker dans cet environnement.

La roadmap suit la logique de développement incrémental définie dans AGENTS.md et la spécification produit. Le projet ne doit pas avancer vers l’étape suivante sans validation de l’architecture de l’étape courante.

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
- exemple de variables d’environnement ;
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
- configuration d’environnement centralisée ;
- variables Docker/PostgreSQL ;
- health checks basiques ;
- documentation de démarrage local ;
- cohérence backend / Docker / uv.

### Non inclus dans cette étape

- modèles SQLAlchemy métier ;
- migrations de persistance ;
- JobOffer, UserProfile, collecteur ou matching ;
- fonction de business logic ;
- toute étape d’implémentation métier.

### État

Configuration mise en place dans le dépôt. Le runtime Docker réel n’a pas pu être validé dans cet environnement car Docker est absent. La synthèse YAML et les vérifications Python effectuées sont correctes, mais le lancement de `docker compose up` reste à exécuter sur une machine avec Docker installé.

---

## Étape 3 — Modèle métier et persistance

### Objectif

Implémenter les premiers modèles de données, repositories et migrations initiales.

### Sous-étapes

- JobSource et RawJobSnapshot ;
- JobOffer et JobOccurrence ;
- UserProfile et UserPreference ;
- Interaction et Application ;
- MatchResult ;
- premières API de lecture/écriture.

### État

Non commencé.

---

## Étape 4 — Collecte et normalisation

### Objectif

Construire le canal d’acquisition des données sources.

### Sous-étapes

- interface commune des sources ;
- collecteur de test / fixtures ;
- parsing et validation ;
- normalisation structurée ;
- stockage des snapshots bruts ;
- gestion des erreurs et des taux de collecte.

---

## Étape 5 — Déduplication et matching déterministe

### Objectif

Faire fonctionner les mécanismes de tri et de recommandation.

### Sous-étapes

- fingerprint et déduplication progressive ;
- matching V1 par composantes ;
- critères éliminatoires ;
- versioning du moteur de scoring ;
- explication des recommandations.

---

## Étape 6 — Frontend MVP

### Objectif

Mettre en place l’interface utilisateur principale.

### Sous-étapes

- écran liste des offres ;
- filtres et recherche ;
- détails d’une offre ;
- profil utilisateur ;
- favoris / rejet / archive ;
- suivi des candidatures.

---

## Étape 7 — Évolution du système

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

- cohérence avec l’architecture décidée ;
- documentation en cours de validité ;
- présence de tests adaptés ;
- absence de sur-ingénierie ;
- respect du périmètre de la step courante.

Le projet reste sur la phase d’infrastructure locale, sans démarrage de l’Étape 3.
