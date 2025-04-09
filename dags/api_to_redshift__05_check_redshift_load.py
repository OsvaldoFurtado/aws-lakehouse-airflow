from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.operators.dummy import DummyOperator

from datetime import datetime



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
    dag_id="check_redshift_load",
    description="Check the Quality of rdshift loaded data",
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    tags=['check-redshift-load'],
    default_args=DEFAULT_ARGS,
)
def check_redshift_load():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")


    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    

    chain(
        begin,
        check_load(),
        end
    )

check_redshift_load()