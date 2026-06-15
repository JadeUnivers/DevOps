# 🏠 Airbnb Analytics Platform

Plateforme analytique Airbnb construite avec **DuckDB**, **dbt** et **Streamlit**.

---

## 📐 Architecture

```
GitHub
  │
  ▼
dbt Project
  │
  ├── Bronze  →  Ingestion brute (CSV → DuckDB)
  ├── Silver  →  Nettoyage, typage, filtrage
  └── Gold    →  Data products & vues analytiques
                        │
                        ▼
                   Streamlit App
                        │
                        ▼
                  Business Users
```

---

## 🗂️ Structure du projet

```
airbnb_analytics/
├── data/                        # ⚠️ Fichiers CSV sources (à télécharger, non versionnés)
├── seeds/
│   ├── seed_full_moon_dates.csv # Dates des pleines lunes
│   └── schema.yml
├── models/
│   ├── bronze/                  # Ingestion brute
│   │   ├── bronze_hosts.sql
│   │   ├── bronze_reviews.sql
│   │   ├── bronze_listings.sql
│   │   └── schema.yml
│   ├── silver/                  # Nettoyage & typage
│   │   ├── silver_hosts.sql
│   │   ├── silver_reviews.sql
│   │   ├── silver_listings.sql
│   │   └── schema.yml
│   └── gold/                    # Data products
│       ├── dim_hosts.sql
│       ├── dim_listings.sql
│       ├── fact_reviews.sql
│       ├── full_moon_reviews.sql
│       └── schema.yml
├── tests/                       # Tests singuliers personnalisés
│   ├── test_no_nulls_in_fact_reviews.sql
│   ├── test_full_moon_values.sql
│   └── test_positive_price.sql
├── macros/
│   └── no_nulls_in_columns.sql
├── scripts/
│   └── load_raw_data.py         # Ingestion initiale Bronze
├── streamlit/
│   └── app.py                   # Dashboard interactif
├── dbt_project.yml
├── profiles.yml
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### Prérequis
- Python 3.10+
- Git
- VS Code (recommandé)

### 1. Cloner le dépôt

```bash
git clone https://github.com/JadeUnivers/DevOps.git
cd airbnb_analytics
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger les données sources

Placez les fichiers suivants dans le dossier `data/` (à créer) :

| Fichier | URL |
|---------|-----|
| `hosts.csv` | https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/hosts.csv |
| `reviews.csv` | https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv |
| `listings.csv` | https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/listings.csv |

> ℹ️ `seed_full_moon_dates.csv` est déjà inclus dans `seeds/`.

---

## 🚀 Exécution

### Étape 1 — Ingestion Bronze (script Python)

```bash
python scripts/load_raw_data.py
```

### Étape 2 — Pipeline dbt complet

```bash
# Vérifier la connexion
dbt debug --profiles-dir .

# Charger les seeds (pleines lunes)
dbt seed --profiles-dir .

# Construire tous les modèles
dbt run --profiles-dir .

# Lancer les tests qualité
dbt test --profiles-dir .

# Générer la documentation
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

### Étape 3 — Dashboard Streamlit

```bash
streamlit run streamlit/app.py
```

Accès : http://localhost:8501

---

## 📊 Fonctionnalités du dashboard

| Page | Description |
|------|-------------|
| 🏠 Vue d'ensemble | KPIs globaux + répartition sentiments |
| 🛏️ Logements | Analyse par type de chambre, prix, filtres dynamiques |
| 👤 Hôtes | Superhosts vs standard, top hôtes |
| ⭐ Avis clients | Filtres par reviewer/sentiment, évolution temporelle |
| 🌕 Impact Pleine Lune | Analyse comparative full moon vs hors lune |

---

## ✅ Tests qualité dbt

| Test | Type | Modèle |
|------|------|--------|
| `not_null` sur les clés primaires | Générique | Bronze, Silver, Gold |
| `unique` sur les IDs | Générique | Hosts, Listings |
| `accepted_values` pour sentiment | Générique | Reviews, full_moon_reviews |
| `accepted_values` pour is_full_moon | Générique | full_moon_reviews |
| `test_no_nulls_in_fact_reviews` | Singulier | fact_reviews |
| `test_full_moon_values` | Singulier | full_moon_reviews |
| `test_positive_price` | Singulier | silver_listings |

---

## 👥 Répartition des tâches

| Membre | Responsabilités |
|--------|----------------|
| David ATCHORI | Couche Bronze, couche Silver, documentation |
| Christ Antony TCHOKOGUEU| Tests qualité, Couche Gold, revues de code |
| Jade DELCOURT | Application Streamlit, README |


---

## 🔧 Technologies

- **DuckDB 0.10** — moteur analytique embarqué
- **dbt-duckdb 1.8** — transformations SQL en pipeline
- **Streamlit 1.35** — dashboard interactif
- **Plotly 5.22** — visualisations
- **GitHub** — versioning & collaboration
