"""
scripts/load_raw_data.py
------------------------
Script d'ingestion des fichiers CSV/JSON bruts dans DuckDB (couche Bronze).
À exécuter UNE FOIS avant `dbt run`, après avoir placé les fichiers dans data/.

Usage :
    python scripts/load_raw_data.py
"""

import duckdb
import os
from pathlib import Path

ROOT     = Path(__file__).parent.parent
DATA_DIR = ROOT / "seeds"
DB_PATH  = ROOT / "airbnb.duckdb"

def check_files():
    required = ["hosts.csv", "listings.csv", "reviews.csv"]
    missing  = [f for f in required if not (DATA_DIR / f).exists()]
    if missing:
        print(f"❌ Fichiers manquants dans seed/ : {missing}")
        print("   Téléchargez-les depuis :")
        print("   https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/")
        raise SystemExit(1)
    print("✅ Tous les fichiers sources sont présents.")

def create_schemas(conn):
    for schema in ["bronze", "silver", "gold"]:
        conn.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
    print("✅ Schémas bronze / silver / gold créés.")

def load_bronze(conn):
    conn.execute(f"""
        CREATE OR REPLACE TABLE bronze.hosts AS
        SELECT * FROM read_csv_auto('{DATA_DIR}/hosts.csv', header=true, all_varchar=true)
    """)
    print(f"   → bronze.hosts : {conn.execute('SELECT COUNT(*) FROM bronze.hosts').fetchone()[0]} lignes")

    conn.execute(f"""
        CREATE OR REPLACE TABLE bronze.reviews AS
        SELECT * FROM read_csv_auto('{DATA_DIR}/reviews.csv', header=true, all_varchar=true)
    """)
    print(f"   → bronze.reviews : {conn.execute('SELECT COUNT(*) FROM bronze.reviews').fetchone()[0]} lignes")

    conn.execute(f"""
        CREATE OR REPLACE TABLE bronze.listings AS
        SELECT * FROM read_csv_auto('{DATA_DIR}/listings.csv', header=true, all_varchar=true)
    """)
    print(f"   → bronze.listings : {conn.execute('SELECT COUNT(*) FROM bronze.listings').fetchone()[0]} lignes")

    print("✅ Couche Bronze chargée.")

def main():
    print("=" * 50)
    print(" Airbnb Analytics — Ingestion Bronze")
    print("=" * 50)
    check_files()

    conn = duckdb.connect(str(DB_PATH))
    create_schemas(conn)
    load_bronze(conn)
    conn.close()
    print(f"\n✅ Base DuckDB prête : {DB_PATH}")
    print("   Lancez maintenant : dbt seed && dbt run")

if __name__ == "__main__":
    main()
