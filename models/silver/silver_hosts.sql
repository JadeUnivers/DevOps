-- models/silver/silver_hosts.sql
-- Couche Silver : nettoyage et typage des hôtes

{{ config(materialized='table') }}

SELECT
    CAST(id AS INTEGER)                          AS host_id,
    COALESCE(NULLIF(TRIM(name), ''), 'Anonymous') AS host_name,
    CASE
        WHEN LOWER(TRIM(is_superhost)) IN ('t', 'true', '1', 'yes') THEN TRUE
        ELSE FALSE
    END                                          AS is_superhost,
    CAST(created_at AS TIMESTAMP)                AS created_at,
    CAST(updated_at AS TIMESTAMP)                AS updated_at
FROM {{ ref('bronze_hosts') }}
WHERE id IS NOT NULL
