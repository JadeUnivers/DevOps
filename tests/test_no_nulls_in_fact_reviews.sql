-- tests/test_no_nulls_in_fact_reviews.sql
-- Test singulier : vérifie que listing_id et review_date ne sont jamais NULL dans fact_reviews

SELECT *
FROM {{ ref('fact_reviews') }}
WHERE listing_id IS NULL
   OR review_date IS NULL
