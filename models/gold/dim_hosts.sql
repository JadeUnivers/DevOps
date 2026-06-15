-- models/gold/dim_hosts.sql
-- Couche Gold : dimension hôtes prête pour l'analyse

{{ config(materialized='view') }}

SELECT
    host_id,
    host_name,
    is_superhost,
    created_at,
    updated_at
FROM {{ ref('silver_hosts') }}
