-- models/bronze/bronze_listings.sql
-- Couche Bronze : ingestion brute des logements depuis le fichier CSV
-- Note : le fichier est nommé listings.csv malgré l'extension .json mentionnée dans le lab

{{ config(materialized='table') }}

SELECT
    id,
    listing_url,
    name,
    room_type,
    minimum_nights,
    host_id,
    price,
    created_at,
    updated_at
FROM read_csv_auto('{{ var("data_path", "data/") }}listings.csv',
    header = true,
    all_varchar = true
)
