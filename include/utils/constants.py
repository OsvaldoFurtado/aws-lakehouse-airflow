import os

JOBS_API_URL = os.getenv("JOBS_API_URL")
JOBS_API_HEADER = os.getenv("JOBS_API_HEADER")
AWS_S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION") 
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BASE_LOCAL_PATH = os.getenv("BASE_LOCAL_PATH")
REDSHIFT_WORKGROUP = os.getenv("REDSHIFT_WORKGROUP")
REDSHIFT_DATABASE = os.getenv("REDSHIFT_DATABASE")
ARN_ROLE = os.getenv("ARN_ROLE")
SCHEMA = os.getenv("REDSHIFT_SCHEMA")

API_FIELDS = (
        "befristung",
        "behinderung",
        "berufsfeld",
        "arbeitsort_plz",
        "arbeitszeit",
        "eintrittsdatum"
)       