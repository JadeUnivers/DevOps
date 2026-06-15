-- tests/test_positive_price.sql
-- Test singulier : vérifie que les prix des logements sont positifs ou NULL

SELECT *
FROM {{ ref('silver_listings') }}
WHERE price IS NOT NULL
  AND price <= 0
