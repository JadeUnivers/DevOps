-- models/silver/silver_reviews.sql
-- Couche Silver : nettoyage et normalisation des avis clients

{{ config(materialized='table') }}

SELECT
    CAST(listing_id AS INTEGER)       AS listing_id,
    CAST(date AS DATE)                AS review_date,
    TRIM(reviewer_name)               AS reviewer_name,
    TRIM(comments)                    AS review_text,
    LOWER(TRIM(sentiment))            AS sentiment
FROM {{ ref('bronze_reviews') }}
WHERE comments IS NOT NULL
  AND TRIM(comments) != ''
