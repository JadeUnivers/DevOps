-- models/bronze/bronze_reviews.sql
-- Couche Bronze : ingestion brute des avis clients depuis le fichier CSV

{{ config(materialized='table') }}

SELECT
    listing_id,
    date,
    reviewer_name,
    comments,
    sentiment
FROM read_csv_auto('{{ var("data_path", "data/") }}reviews.csv',
    header = true,
    all_varchar = true
)
