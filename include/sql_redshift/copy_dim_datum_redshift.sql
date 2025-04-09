COPY '{{ params.schema }}'.dim_datum (
    datum_id, 
    datum, 
    woche, 
    tag_woche, 
    monat, 
    monat_bz, 
    quartal, 
    jahr
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER '{{ params.delimiter }}'
IGNOREHEADER 1;