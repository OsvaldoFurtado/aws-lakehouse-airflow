BEGIN TRANSACTION;

DELETE
FROM '{{ params.schema }}'.berufsfeld
    USING '{{ params.schema }}'.berufsfeld_staging
WHERE berufsfeld.datum_id = '{{ params.datum_id }}';

INSERT INTO '{{ params.schema }}'.berufsfeld
SELECT
    '{{ params.datum_id }}',
    berufsfeld,
    count
FROM '{{ params.schema }}'.berufsfeld_staging;

END TRANSACTION;