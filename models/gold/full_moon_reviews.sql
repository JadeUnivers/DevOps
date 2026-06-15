-- models/gold/full_moon_reviews.sql
-- Couche Gold : data product - impact des nuits de pleine lune sur les avis

{{ config(materialized='table') }}

SELECT
    fr.*,
    CASE
        WHEN fm.full_moon_date IS NULL THEN 'not full moon'
        ELSE 'full moon'
    END AS is_full_moon
FROM {{ ref('fact_reviews') }} fr
LEFT JOIN {{ ref('seed_full_moon_dates') }} fm
    ON fr.review_date = (fm.full_moon_date::DATE + INTERVAL '1 day')
