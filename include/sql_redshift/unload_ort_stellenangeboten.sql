UNLOAD ('
    SELECT
        o.datum_id,
        d.datum,
        d.woche,
        d.tag_woche,
        d.monat,
        d.monat_bz,
        d.quartal,
        d.jahr,
        o.arbeitsort_plz,
        p.place,
        p.state,
        p.latitude,
        p.longitude,
        o.count
    FROM '{{ params.schema }}'.arbeitsort_plz AS o
    LEFT JOIN '{{ params.schema }}'.dim_datum AS d ON o.datum_id = d.datum_id
    LEFT JOIN '{{ params.schema }}'.dim_zipcode AS p ON o.arbeitsort_plz = p.zipcode
')
TO '{{ params.s3_unload_path }}'
IAM_ROLE '{{ params.redshift_unload_iam_role }}'
PARQUET PARTITION BY (state) CLEANPATH;