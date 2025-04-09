
from datetime import datetime


from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator


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
    dag_id="api_to_s3",
    description="Get data from API save locally and upload to s3",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=['extract-api-s3'],
    template_searchpath='/usr/local/airflow/include/sql_redshift'
)
def extract_api_to_s3():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")


    @task.external_python(python='/usr/local/airflow/pandas_venv/bin/python')
    def extract_api_data():

        from include.pipelines.api_pipeline import extract_and_save_local
        
        #extract data from api and save locally on csv files
        extract_and_save_local()


    @task.external_python(python='/usr/local/airflow/aws_venv/bin/python')
    def upload_to_s3():

        from include.pipelines.aws_s3_pipeline import upload_s3_pipeline
        upload_s3_pipeline()

 
    chain(
        begin,
        extract_api_data(),
        upload_to_s3(),
        end
    )

extract_api_to_s3()

