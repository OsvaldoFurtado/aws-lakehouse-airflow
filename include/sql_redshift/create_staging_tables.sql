BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.arbeitsort_plz_staging
(
    arbeitsort_plz varchar(10) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.arbeitszeit_staging
(
    arbeitszeit varchar(50) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.befristung_staging
(
    befristung varchar(30) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.behinderung_staging
(
    behinderung boolean NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.berufsfeld_staging
(
    berufsfeld varchar(200) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.eintrittsdatum_staging
(
    eintrittsjahr smallint NOT NULL,
    eintrittsmonat smallint NOT NULL,
    count integer NOT NULL
);

END TRANSACTION;
