BEGIN TRANSACTION;

DELETE
FROM '{{ params.schema }}'.arbeitszeit
    USING '{{ params.schema }}'.arbeitszeit_staging
WHERE arbeitszeit.datum_id = '{{ params.datum_id }}';

INSERT INTO '{{ params.schema }}'.arbeitszeit
SELECT
    '{{ params.datum_id }}',
    arbeitszeit,
    count
FROM '{{ params.schema }}'.arbeitszeit_staging;

END TRANSACTION;