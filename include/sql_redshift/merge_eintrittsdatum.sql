BEGIN TRANSACTION;

DELETE
FROM stelle.eintrittsdatum
    USING stelle.eintrittsdatum_staging
WHERE eintrittsdatum.datum_id = '{{ params.datum_id }}';

INSERT INTO stelle.eintrittsdatum
SELECT
    '{{ params.datum_id }}',
    eintrittsjahr,
    eintrittsmonat,
    count
FROM stelle.eintrittsdatum_staging;

END TRANSACTION;