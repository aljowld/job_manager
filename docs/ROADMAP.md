# Roadmap du projet

Statut actuel : Étape 1 — Bootstrap du repository terminé.

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

Ce document et les ADR associés définissent l’état de référence pour l’étape 0.

### État

Ceci est désormais validé et documenté dans [docs/ARCHITECTURE.md](ARCHITECTURE.md) et les ADRs associés.

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

### Non inclus dans cette étape

- aucun modèle métier ;
- aucune base PostgreSQL ;
- aucun collecteur ;
- aucun moteur de matching ;
- aucune fonctionnalité des étapes suivantes.

---

## Étape 2 — Modèle métier et persistance

### Objectif

Implémenter les premiers modèles de données, repositories et migrations initiales.

### Sous-étapes

- JobSource et RawJobSnapshot ;
- JobOffer et JobOccurrence ;
- UserProfile et UserPreference ;
- Interaction et Application ;
- MatchResult ;
- premières API de lecture/écriture.

---

## Étape 2 — Modèle métier et persistance

### Objectif

Implémenter les premiers modèles de données, repositories et migrations initiales.

### Sous-étapes

- JobSource et RawJobSnapshot ;
- JobOffer et JobOccurrence ;
- UserProfile et UserPreference ;
- Interaction et Application ;
- MatchResult ;
- premières API de lecture/écriture.

---

## Étape 3 — Collecte et normalisation

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

## Étape 4 — Déduplication et matching déterministe

### Objectif

Faire fonctionner les mécanismes de tri et de recommandation.

### Sous-étapes

- fingerprint et déduplication progressive ;
- matching V1 par composantes ;
- critères éliminatoires ;
- versioning du moteur de scoring ;
- explication des recommandations.

---

## Étape 5 — Frontend MVP

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

## Étape 6 — Évolution du système

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

Le projet est actuellement à l’arrêt de la roadmap au niveau d’architecture. L’étape 1 n’est pas commencée dans ce lot de travail.
