-- models/gold/dim_listings.sql
-- Couche Gold : dimension logements enrichie

{{ config(materialized='view') }}

SELECT
    l.listing_id,
    l.listing_url,
    l.listing_name,
    l.room_type,
    l.minimum_nights,
    l.host_id,
    l.price,
    l.created_at,
    l.updated_at,
    h.host_name,
    h.is_superhost
FROM {{ ref('silver_listings') }} l
LEFT JOIN {{ ref('silver_hosts') }} h
    ON l.host_id = h.host_id
