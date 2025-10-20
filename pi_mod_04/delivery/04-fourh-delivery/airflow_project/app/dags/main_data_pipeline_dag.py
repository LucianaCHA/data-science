from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.amazon.aws.transfers.s3_to_s3 import S3CopyObjectOperator
from datetime import datetime, timedelta

PATH = "/home/ubuntu/spark_project"
DOCKER_COMMAND = "sudo docker-compose up --build --abort-on-container-exit"

AIRBYTE_CONN_ID = "airbyte_cloud_conn"
AIRBYTE_CONNECTION_ID = "0a22aba7-23a8-4d86-ab33-4f8522a90ee0"

SPARK_CONN_ID = "spark-ec2-ssh"
SPARK_DOCKER_COMMAND = f"cd {PATH} && {DOCKER_COMMAND}"


def subdag_airbyte_sync(parent_dag_name, child_dag_name, args):
    dag_id = f"{parent_dag_name}.{child_dag_name}"
    with DAG(
        dag_id=dag_id,
        default_args=args,
        schedule_interval=None,
    ) as subdag:
        run_airbyte_sync = AirbyteTriggerSyncOperator(
            task_id="run_airbyte_sync",
            airbyte_conn_id=AIRBYTE_CONN_ID,
            connection_id=AIRBYTE_CONNECTION_ID,
            asynchronous=False,
            timeout=3600,
            wait_seconds=30,
        )
        _ = run_airbyte_sync
    return subdag


def subdag_spark_transformation(parent_dag_name, child_dag_name, args):
    dag_id = f"{parent_dag_name}.{child_dag_name}"
    with DAG(
        dag_id=dag_id,
        default_args=args,
        schedule_interval=None,
    ) as subdag:
        run_spark_job = SSHOperator(
            task_id="run_spark_job",
            ssh_conn_id=SPARK_CONN_ID,
            command=SPARK_DOCKER_COMMAND,
            cmd_timeout=1800,
        )
        _ = run_spark_job
    return subdag


def subdag_move_to_gold(parent_dag_name, child_dag_name, args):
    dag_id = f"{parent_dag_name}.{child_dag_name}"
    with DAG(
        dag_id=dag_id,
        default_args=args,
        schedule_interval=None,
    ) as subdag:
        move_to_gold_layer = S3CopyObjectOperator(
            task_id="move_to_gold_layer",
            source_bucket_name="processed-data-bucket",
            source_key="gold/enriched_weather_data",
            dest_key="gold/",
            aws_conn_id="aws_default",
        )
        _ = move_to_gold_layer
    return subdag


default_args = {
    "owner": "luciana",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1),
}


with DAG(
    dag_id="main_data_pipeline_dag",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    tags=["data-pipeline"],
) as dag:

    start = DummyOperator(task_id="start")

    airbyte_sync = SubDagOperator(
        task_id="airbyte_sync_subdag",
        subdag=subdag_airbyte_sync(
            "main_data_pipeline_dag", "airbyte_sync_subdag", default_args
        ),
        dag=dag,
    )

    spark_transformation = SubDagOperator(
        task_id="spark_transformation_subdag",
        subdag=subdag_spark_transformation(
            "main_data_pipeline_dag", "spark_transformation_subdag", default_args
        ),
        dag=dag,
    )

    move_to_gold = SubDagOperator(
        task_id="move_to_gold_subdag",
        subdag=subdag_move_to_gold(
            "main_data_pipeline_dag", "move_to_gold_subdag", default_args
        ),
        dag=dag,
    )

    end = DummyOperator(task_id="end")

    start >> airbyte_sync >> spark_transformation >> move_to_gold >> end
