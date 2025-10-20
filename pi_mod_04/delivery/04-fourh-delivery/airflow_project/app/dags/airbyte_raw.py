from airflow import DAG
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from datetime import datetime

CONN_ID = "airbyte_cloud_conn"
CONNECTION_ID = "0a22aba7-23a8-4d86-ab33-4f8522a90ee0"

default_args = {
    "owner": "luciana",
    "start_date": datetime(2024, 1, 1),
}

with DAG(
    dag_id="airbyte_cloud_sync_weather",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["airbyte", "cloud", "etl"],
) as dag:

    run_airbyte_sync = AirbyteTriggerSyncOperator(
        task_id="run_airbyte_sync",
        airbyte_conn_id=CONN_ID,
        connection_id=CONNECTION_ID,
        asynchronous=False,
        timeout=3600,
        wait_seconds=30,
    )
    run_airbyte_sync
