# ADR-001 : monolithe modulaire, pas microservices

- Date : 2026-08-29
- Statut : acceptée

## Contexte

Le projet doit centraliser des offres d’emploi, les normaliser, les comparer à un profil, et suivre des candidatures. La complexité est forte au niveau métier, mais le besoin immédiat n’est pas un système distribué. Le projet est personnel et doit rester simple à développer, tester et faire évoluer.

## Décision

Nous adoptons un monolithe modulaire, avec des domaines métier clairement identifiés au sein d’un unique backend Python / FastAPI.

Le backend est découpé en modules métier tels que :

- jobs ;
- profile ;
- applications ;
- interactions ;
- collection ;
- normalization ;
- deduplication ;
- matching ;
- enrichment ;
- ai.

Le frontend est séparé dans un application React + TypeScript avec Vite.

La base PostgreSQL reste unique et centrale.

## Conséquences

### Positives

- développement plus rapide ;
- déploiement local plus simple ;
- tests plus cohérents ;
- architecture lisible sans surcharge opérationnelle ;
- possibilité de faire évoluer le système vers un découpage plus fin si nécessaire.

### Négatives / risques

- le monolithe peut devenir large si le projet grandit sans discipline ;
- les dépendances entre modules doivent être maîtrisées ;
- l’équipe doit maintenir une séparation claire des responsabilités.

## Limites

Cette décision est valable pour le MVP. Elle pourra être revue si le besoin de scalabilité, de workers distants ou de sous-systèmes très indépendants devient réel.
