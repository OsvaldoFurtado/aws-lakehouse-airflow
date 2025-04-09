from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator


from datetime import datetime
from include.utils.constants import AWS_S3_BUCKET_NAME, REDSHIFT_WORKGROUP, REDSHIFT_DATABASE, ARN_ROLE, AWS_REGION, SCHEMA



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
    dag_id="unload_redshift_data",
    description="Unload complete arbeitsort data to create a report",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    tags=['redshift-s3-arbeitsort'],
    default_args=DEFAULT_ARGS,
    template_searchpath='/usr/local/airflow/include/sql_redshift'
)
def unload_redshift_data():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")

    unload_redshift_data = RedshiftDataOperator(
        task_id="unload_redshift_data",
        sql="unload_ort_stellenangeboten.sql",
        params={
            "schema": SCHEMA,
            "s3_unload_path": f"s3://{AWS_S3_BUCKET_NAME}/redshift/arbeitsort/",
            "redshift_unload_iam_role": ARN_ROLE
        },
        aws_conn_id='aws_default',
        workgroup_name=REDSHIFT_WORKGROUP,
        database=REDSHIFT_DATABASE,
        wait_for_completion=True,
        region_name=AWS_REGION
    )    

    chain(
        begin,
        unload_redshift_data,
        end
    )

unload_redshift_data()