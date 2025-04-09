COPY '{{ params.schema }}'.dim_zipcode (
    zipcode, 
    place, 
    state, 
    state_code, 
    community, 
    community_code, 
    latitude, 
    longitude
)
FROM '{{ params.bucket_path }}'
IAM_ROLE '{{ params.iam_role }}'
FORMAT AS CSV
DELIMITER '{{ params.delimiter }}'
IGNOREHEADER 1;