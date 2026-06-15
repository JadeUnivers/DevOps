-- models/bronze/bronze_hosts.sql
-- Couche Bronze : ingestion brute des hôtes depuis le fichier CSV

{{ config(materialized='table') }}

SELECT
    id,
    name,
    is_superhost,
    created_at,
    updated_at
FROM read_csv_auto('{{ var("data_path", "data/") }}hosts.csv',
    header = true,
    all_varchar = true
)
