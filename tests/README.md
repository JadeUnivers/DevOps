# Tests du projet Airbnb Analytics

## Objectif
Ce dossier contient les tests de qualité des données.

## Types de tests

### 1. Valeurs NULL
Vérifie qu’il n’y a pas de valeurs manquantes dans les tables critiques.

### 2. Prix positifs
Vérifie que les prix sont toujours supérieurs à 0.

### 3. Cohérence des données
Assure la fiabilité des analyses.

## Exécution
```bash
dbt test