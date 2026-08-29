# ADR-003 : moteur de matching déterministe en V1

- Date : 2026-08-29
- Statut : acceptée

## Contexte

Le cœur du produit est de comparer les offres à un profil utilisateur et d’expliquer pourquoi une offre est pertinente. Une logique opaque ou fondée sur des modèles externes trop tôt introduirait une perte de fiabilité et de reproductibilité.

## Décision

Le moteur de matching V1 est entièrement déterministe. Il est basé sur :

- critères bien définis ;
- pondération explicite par composante ;
- seuils de compatibilité configurables ;
- séparation entre score et critères éliminatoires ;
- gestion explicite de MATCH / MISMATCH / UNKNOWN ;
- version du moteur pour chaque calcul.

Le score est calculé selon une formule de type :

```text
final_score = Σ(component_score × component_weight)
```

Le moteur reste explicable, reproductible et testable sans dépendance à un modèle IA.

## Conséquences

### Positives

- décisions plus compréhensibles ;
- meilleure qualité de test ;
- réduction des biais d’un modèle opaque ;
- base solide pour enrichissements ultérieurs ;
- capacité à comparer des versions de moteur entre elles.

### Négatives / risques

- moins de finesse immédiate qu’un modèle d’IA ;
- besoin de bonnes données structurées et normalisées ;
- certains cas ambigus requerront une évolution ultérieure.

## Limites

L’IA ou la recherche vectorielle n’est pas exclue, mais elle vient après la stabilisation d’un moteur déterministe et explicable. Cette décision est la base de la recommandation métier.
