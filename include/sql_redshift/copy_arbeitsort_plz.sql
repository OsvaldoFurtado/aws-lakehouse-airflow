COPY '{{ params.schema }}'.arbeitsort_plz_staging (
    arbeitsort_plz, 
    count
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER ','
IGNOREHEADER 1;