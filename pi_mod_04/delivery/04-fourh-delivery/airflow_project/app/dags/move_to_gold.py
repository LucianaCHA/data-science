from airflow import DAG
from airflow.providers.amazon.aws.transfers.s3_to_s3 import S3CopyObjectOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'luciana',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 1, 1),
}

with DAG(
    dag_id="move_to_gold_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["s3", "gold-layer"],
) as dag:

    move_to_gold_layer = S3CopyObjectOperator(
        task_id="move_to_gold_layer",
        source_bucket_name="processed-data-bucket",
        source_key="processed/*",
        dest_bucket_name="gold-data-bucket",
        dest_key="gold/",
        aws_conn_id="aws_default",
    )
