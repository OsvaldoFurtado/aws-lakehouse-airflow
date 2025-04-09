
from datetime import datetime
from include.utils.constants import AWS_S3_BUCKET_NAME, REDSHIFT_WORKGROUP, REDSHIFT_DATABASE, ARN_ROLE, AWS_REGION
import os

from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator
from airflow.operators.dummy import DummyOperator


year = datetime.now().strftime("%Y") #2025
month = datetime.now().strftime("%m") #04
day = datetime.now().strftime("%d") #08



SCHEMA = "stelle"
TABLES = {
        "arbeitsort_plz": ["arbeitsort_plz","count"],
        "arbeitszeit": ["arbeitszeit","count"],
        "befristung": ["befristung", "count"],
        "behinderung": ["behinderung","count"],
        "berufsfeld": ["berufsfeld","count"],
        "eintrittsdatum": ["eintrittsjahr", "eintrittsmonat","count"]
}


DEFAULT_ARGS = {
    "owner": "osvaldofurtado",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
    "redshift_conn_id": "redshift_default",
    "postgres_conn_id": "redshift_default",
}


@dag(
    dag_id="s3_to_redshift_daily",
    description="Load daily fact tables data from s3 to redshift",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    tags=['s3-redshift-daily'],
    default_args=DEFAULT_ARGS,
    template_searchpath='/usr/local/airflow/include/sql_redshift'
)
def load_s3_redshift_daily():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")


    for table in TABLES:
          

        truncate_staging_tables = RedshiftDataOperator(
            task_id=f"truncate_table_{table}_staging",
            sql=f"TRUNCATE TABLE {SCHEMA}.{table}_staging;",
            aws_conn_id='aws_default',
            workgroup_name=REDSHIFT_WORKGROUP,
            database=REDSHIFT_DATABASE,
            wait_for_completion=True,
            region_name=AWS_REGION
        )


        s3_to_staging_tables = RedshiftDataOperator(
            task_id=f"copy_table_{table}",
            sql=f"copy_{table}.sql",
            params={
                "schema": SCHEMA,
                "bucket_path": f"s3://{AWS_S3_BUCKET_NAME}/raw/year={year}/month={month}/day={day}/{table}.csv",
                "iam_role": ARN_ROLE
            },
            aws_conn_id='aws_default',
            workgroup_name=REDSHIFT_WORKGROUP,
            database=REDSHIFT_DATABASE,
            wait_for_completion=True,
            region_name=AWS_REGION
        )    


        merge_staging_final_tables = RedshiftDataOperator(
            task_id=f"merge_table_{table}",
            sql=f"merge_{table}.sql",
            params={
                "datum_id": f"{year}{month}{day}",
                "schema": SCHEMA
            },
            aws_conn_id='aws_default',
            workgroup_name=REDSHIFT_WORKGROUP,
            database=REDSHIFT_DATABASE,
            wait_for_completion=True,
            region_name=AWS_REGION
        )


        chain(
            begin,
            truncate_staging_tables,
            s3_to_staging_tables,
            merge_staging_final_tables,
            end
        )

load_s3_redshift_daily()

