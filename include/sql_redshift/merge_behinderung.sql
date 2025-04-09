BEGIN TRANSACTION;

DELETE
FROM '{{ params.schema }}'.behinderung
    USING '{{ params.schema }}'.behinderung_staging
WHERE behinderung.datum_id = '{{ params.datum_id }}';

INSERT INTO '{{ params.schema }}'.behinderung
SELECT
    '{{ params.datum_id }}',
    behinderung,
    count
FROM '{{ params.schema }}'.behinderung_staging;

END TRANSACTION;