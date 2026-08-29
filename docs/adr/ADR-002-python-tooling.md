# ADR-002 : uv, Ruff et ty comme outils de référence du backend

- Date : 2026-08-29
- Statut : acceptée

## Contexte

Le projet doit fournir un environnement Python cohérent, reproductible et vérifiable. Les dépendances ne doivent pas reposer sur plusieurs systèmes concurrentiels, et le backend doit rester maintenable avec un niveau de qualité strict.

## Décision

Le backend Python utilise exclusivement :

- uv comme gestionnaire de projet et d’environnement ;
- Ruff pour le linting et le formatage ;
- ty pour la vérification statique des types ;
- pytest pour les tests backend ;
- uv.lock versionné dans Git.

Le quality gate appliqué au backend est :

```bash
uv lock --check
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

## Conséquences

### Positives

- environnement unifié local / CI / Docker ;
- dépendances verrouillées ;
- qualité de code contrôlée par des standards explicites ;
- meilleur typage et réduction des erreurs de contrat.

### Négatives / risques

- apprentissage plus nécessaire pour le développeur si son environnement était basé sur pip ou autre solution ;
- configuration initiale plus stricte et exigente.

## Notes

Cette décision est structurante et ne doit pas être contournée sans une revue d’architecture. Le projet ne doit pas mélanger uv avec des workflows de dépendances parallèles.
