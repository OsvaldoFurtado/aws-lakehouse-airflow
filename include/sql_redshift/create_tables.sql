BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.arbeitsort_plz
(
    datum_id integer NOT NULL SORTKEY,
    arbeitsort_plz varchar(10) NOT NULL DISTKEY,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.arbeitszeit
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    arbeitszeit varchar(50) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.befristung
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    befristung varchar(30) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.behinderung
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    behinderung boolean NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.berufsfeld
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    berufsfeld varchar(200) NOT NULL,
    count integer NOT NULL
);

CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.eintrittsdatum
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    eintrittsjahr integer NOT NULL,
    eintrittsmonat smallint NOT NULL,
    count integer NOT NULL
);


CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.dim_zipcode
(
    zipcode varchar(10) NOT NULL DISTKEY SORTKEY,
    place varchar(200) NOT NULL,
    state varchar(100) NOT NULL,
    state_code char(5) NOT NULL,
    community varchar(100),
    community_code varchar(20),
    latitude decimal(8,4),
    longitude decimal(8,4)
);


CREATE TABLE IF NOT EXISTS '{{ params.schema }}'.dim_datum
(
    datum_id integer NOT NULL DISTKEY SORTKEY,
    datum smallint NOT NULL,
    woche smallint NOT NULL,
    tag_woche char(2) NOT NULL,
    monat smallint NOT NULL,
    monat_bz varchar(10) NOT NULL,
    quartal smallint NOT NULL,
    jahr smallint NOT NULL
);

END TRANSACTION;



