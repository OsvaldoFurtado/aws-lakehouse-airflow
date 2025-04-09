COPY '{{ params.schema }}'.eintrittsdatum_staging (
    eintrittsjahr, 
    eintrittsmonat,
    count
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1;