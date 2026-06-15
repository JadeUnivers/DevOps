-- models/gold/fact_reviews.sql
-- Couche Gold : table de faits des avis clients (uniquement avis non NULL)

{{ config(materialized='table') }}

SELECT
    r.listing_id,
    r.review_date,
    r.reviewer_name,
    r.review_text,
    r.sentiment,
    l.listing_name,
    l.room_type,
    l.price,
    l.host_id,
    h.host_name,
    h.is_superhost
FROM {{ ref('silver_reviews') }} r
LEFT JOIN {{ ref('silver_listings') }} l
    ON r.listing_id = l.listing_id
LEFT JOIN {{ ref('silver_hosts') }} h
    ON l.host_id = h.host_id
ORDER BY r.review_date DESC
