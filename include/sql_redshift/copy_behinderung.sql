COPY '{{ params.schema }}'.behinderung_staging (
    behinderung, 
    count
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1;