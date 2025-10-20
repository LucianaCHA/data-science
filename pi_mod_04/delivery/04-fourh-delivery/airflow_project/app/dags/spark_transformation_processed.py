from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime, timedelta

SSH_CONN_ID = "spark-ec2-ssh"
SPARK_PROJECT_PATH = "/home/ubuntu/spark_project"
DOCKER_COMMAND = "sudo docker-compose up --build --abort-on-container-exit"

default_args = {
    "owner": "luciana",
    "depends_on_past": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2025, 1, 1),
}

with DAG(
    dag_id="spark_data_transformation_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=["spark", "data-transformation"],
) as dag:

    run_spark_job = SSHOperator(
        task_id="run_spark_job",
        ssh_conn_id=SSH_CONN_ID,
        command=f"cd {SPARK_PROJECT_PATH} && {DOCKER_COMMAND}",
        cmd_timeout=1800,
    )
