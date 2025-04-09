
from datetime import datetime
from include.utils.constants import AWS_S3_BUCKET_NAME, ARN_ROLE, REDSHIFT_WORKGROUP, REDSHIFT_DATABASE, AWS_REGION, SCHEMA
import os

from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from airflow.operators.dummy import DummyOperator


INITIAL_TABLES = {
    "dim_datum": {
        "delimiter": ";"
    }, 
    "dim_zipcode": {
         "delimiter": ","
    }
}


DEFAULT_ARGS = {
    "owner": "osvaldofurtado",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
    "redshift_conn_id": "redshift_default",
    "aws_conn_id": "aws_default",
}


@dag(
    dag_id="s3_to_redshift_initial_data",
    description="Load the dimension tables data",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    tags=['load-s3-redshift-initial-data'],
    default_args=DEFAULT_ARGS,
    template_searchpath='/usr/local/airflow/include/sql_redshift'
)
def load_s3_redshift_initial_data():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")



    for table in INITIAL_TABLES.keys():

        s3_to_redshift_initial_data = RedshiftDataOperator(
            task_id=f"copy_table_{table}",
            sql=f"copy_{table}_redshift.sql",
            params={
                "schema": SCHEMA,
                "bucket_path": f"s3://{AWS_S3_BUCKET_NAME}/raw/initial_data/{table}.csv",
                "iam_role": ARN_ROLE,
                "delimiter": INITIAL_TABLES[table]["delimiter"]
            },
            aws_conn_id='aws_default',
            workgroup_name=REDSHIFT_WORKGROUP,
            database=REDSHIFT_DATABASE,
            wait_for_completion=True,
            region_name=AWS_REGION
        )    


        chain(
            begin,
            s3_to_redshift_initial_data,
            end
        )

load_s3_redshift_initial_data()

