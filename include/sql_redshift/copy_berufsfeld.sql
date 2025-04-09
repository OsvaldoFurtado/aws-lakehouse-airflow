COPY '{{ params.schema }}'.berufsfeld_staging (
    berufsfeld, 
    count
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1;