-- models/silver/silver_listings.sql
-- Couche Silver : nettoyage et typage des logements

{{ config(materialized='table') }}

SELECT
    CAST(id AS INTEGER)                                     AS listing_id,
    TRIM(listing_url)                                       AS listing_url,
    TRIM(name)                                              AS listing_name,
    TRIM(room_type)                                         AS room_type,
    CASE
        WHEN CAST(minimum_nights AS INTEGER) IS NULL THEN 1
        WHEN CAST(minimum_nights AS INTEGER) = 0     THEN 1
        ELSE CAST(minimum_nights AS INTEGER)
    END                                                     AS minimum_nights,
    CAST(host_id AS INTEGER)                                AS host_id,
    CAST(
        REGEXP_REPLACE(REPLACE(price, '$', ''), '[^0-9.]', '')
    AS DOUBLE)                                              AS price,
    CAST(created_at AS TIMESTAMP)                           AS created_at,
    CAST(updated_at AS TIMESTAMP)                           AS updated_at
FROM {{ ref('bronze_listings') }}
WHERE id IS NOT NULL
