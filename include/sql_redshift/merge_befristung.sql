BEGIN TRANSACTION;

DELETE
FROM '{{ params.schema }}'.befristung
    USING '{{ params.schema }}'.befristung_staging
WHERE befristung.datum_id = '{{ params.datum_id }}';

INSERT INTO '{{ params.schema }}'.befristung
SELECT
    '{{ params.datum_id }}',
    befristung,
    count
FROM '{{ params.schema }}'.befristung_staging;

END TRANSACTION;