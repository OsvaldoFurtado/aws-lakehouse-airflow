from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from airflow.decorators import dag
from airflow.models.baseoperator import chain


DEFAULT_ARGS = {
    "owner": "osvaldofurtado",
    "depends_on_past": False,
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
}


@dag(
    start_date=datetime(2024, 9, 29),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    tags=['jobsuche-trigger-dags'],
)
def trigger_dags():

    begin = DummyOperator(task_id="begin")

    end = DummyOperator(task_id="end")


    trigger_dag_01 = TriggerDagRunOperator(
        task_id="trigger_dag_01",
        trigger_dag_id="api_to_s3",
        wait_for_completion=True,
    )
    
    
    trigger_dag_02 = TriggerDagRunOperator(
        task_id="trigger_dag_02",
        trigger_dag_id="create_redshift_tables",
        wait_for_completion=True,
    )


    trigger_dag_03 = TriggerDagRunOperator(
        task_id="trigger_dag_03",
        trigger_dag_id="s3_to_redshift_initial_data",
        wait_for_completion=True,
    )


    trigger_dag_04 = TriggerDagRunOperator(
        task_id="trigger_dag_04",
        trigger_dag_id="s3_to_redshift_daily",
        wait_for_completion=True,
    )


    trigger_dag_05 = TriggerDagRunOperator(
        task_id="trigger_dag_05",
        trigger_dag_id="check_redshift_load",
        wait_for_completion=True,
    )


    trigger_dag_06 = TriggerDagRunOperator(
        task_id="trigger_dag_06",
        trigger_dag_id="unload_redshift_data",
        wait_for_completion=True,
    )


    chain(
        begin,
        trigger_dag_01,
        trigger_dag_02,
        trigger_dag_03,
        trigger_dag_04,
        trigger_dag_05,
        trigger_dag_06,
        end
    )


trigger_dags()