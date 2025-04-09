
from datetime import datetime
import os
from include.utils.constants import REDSHIFT_WORKGROUP, REDSHIFT_DATABASE, AWS_REGION, SCHEMA, AWS_S3_BUCKET_NAME


from airflow.decorators import dag
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator
from airflow.providers.amazon.aws.operators.redshift_data import RedshiftDataOperator


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
    dag_id="create_redshift_tables",
    description="Create redshift tables",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    tags=['jobsuche_create_redshift_tables'],
    default_args=DEFAULT_ARGS,
    template_searchpath='/usr/local/airflow/include/sql_redshift'
)
def create_redshift_final_tables():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")


    create_redshift_tables = RedshiftDataOperator(
        task_id=f"create_redshift_tables",
        sql=f"/create_tables.sql",
        params={"schema": SCHEMA },
        aws_conn_id='aws_default',
        workgroup_name=REDSHIFT_WORKGROUP,
        database=REDSHIFT_DATABASE,
        wait_for_completion=True,
        region_name=AWS_REGION
    )

    create_redshift_staging_tables = RedshiftDataOperator(
        task_id=f"create_redshift_staging_tables",
        sql=f"/create_staging_tables.sql",
        params={"schema": SCHEMA },
        aws_conn_id='aws_default',
        workgroup_name=REDSHIFT_WORKGROUP,
        database=REDSHIFT_DATABASE,
        wait_for_completion=True,
        region_name=AWS_REGION
    )
 
    

    chain(
        begin,
        create_redshift_tables,
        create_redshift_staging_tables,
        end
    )

create_redshift_final_tables()

