from include.etls.aws_s3_etl import connect_to_s3, upload_to_s3
from datetime import datetime
import os
from include.utils.constants import BASE_LOCAL_PATH, AWS_S3_BUCKET_NAME


def upload_s3_pipeline():
    

    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")

    local_init_data_path = f'{BASE_LOCAL_PATH}/dim_data/'
    local_daily_file_path = f'{BASE_LOCAL_PATH}/year={year}/month={month}/day={day}/'

    target_init_data_s3_path = f's3://{AWS_S3_BUCKET_NAME}/raw/dim_data/'
    target_daily_data_s3_path = f's3://{AWS_S3_BUCKET_NAME}/raw/year={year}/month={month}/day={day}/'

    # Create s3 connection
    s3 = connect_to_s3()

    # Upload initial data
    upload_to_s3(s3, local_init_data_path, target_init_data_s3_path)

    # Upload daily data
    upload_to_s3(s3, local_daily_file_path, target_daily_data_s3_path)


if __name__ == "__main__":
    upload_s3_pipeline()