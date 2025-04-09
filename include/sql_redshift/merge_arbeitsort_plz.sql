BEGIN TRANSACTION;

DELETE
FROM '{{ params.schema }}'.arbeitsort_plz
    USING '{{ params.schema }}'.arbeitsort_plz_staging
WHERE arbeitsort_plz.datum_id = '{{ params.datum_id }}';

INSERT INTO '{{ params.schema }}'.arbeitsort_plz
SELECT
    '{{ params.datum_id }}',
    arbeitsort_plz,
    count
FROM '{{ params.schema }}'.arbeitsort_plz_staging;

END TRANSACTION;