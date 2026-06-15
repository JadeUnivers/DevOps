-- tests/test_full_moon_values.sql
-- Test singulier : vérifie que is_full_moon ne contient que les deux valeurs attendues

SELECT *
FROM {{ ref('full_moon_reviews') }}
WHERE is_full_moon NOT IN ('full moon', 'not full moon')
