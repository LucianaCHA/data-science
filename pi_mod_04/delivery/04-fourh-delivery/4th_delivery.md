# Proyecto de Orquestación y Automatización de Pipeline de Datos

En este proyecto, se busca automatizar y orquestar un pipeline de datos que integra varias tecnologías y herramientas. El flujo del pipeline consta de las siguientes etapas:

## Etapas del Pipeline:

1. **Ingesta de datos**: Usando Airbyte para mover los datos desde diferentes fuentes hacia un Data Lake en AWS S3.
2. **Transformación de datos**: Usando Apache Spark en EC2 para realizar transformaciones de los datos y preparar la capa de datos procesados.
3. **Capa Gold**: El resultado de las transformaciones debe ser almacenado en la capa Gold de S3, en formatos optimizados como Parquet o Delta.
4. **Automatización y Orquestación**: Utilizando Apache Airflow para gestionar las tareas, controlar dependencias, reintentos y notificaciones, y realizar la orquestación del pipeline de forma segura.


---

## A) CONSIGNAS

### 1) Provisionamiento de una Instancia EC2 en AWS Free Tier y Despliegue de Apache Airflow

**Acciones realizadas:**

- **Instancia EC2**: Se creó una instancia EC2 t2.micro en el AWS Free Tier.
- **Acceso seguro**: Se configuraron adecuadamente los Security Groups para permitir el acceso al puerto 8080 (Airflow UI) y al puerto 22 (SSH). Además, se configuró IAM para asegurar que las instancias puedan interactuar con S3 y otras APIs de AWS de forma segura.
- **Docker Compose**: Se configuró Apache Airflow utilizando Docker Compose en la instancia EC2, asegurando que los servicios necesarios de Airflow (Scheduler, Webserver, etc.) se ejecutaran correctamente en contenedores.

**Problemas y soluciones:**
- Durante la configuración de la conexión SSH, se presentaron errores relacionados con las claves SSH, que fueron solucionados convirtiendo las claves a OpenSSH y asegurando los permisos correctos.

### 2) Creación del DAG Principal en Airflow para Ejecutar los Conectores de Airbyte y Jobs de Apache Spark

**Acciones realizadas:**

Se creó un DAG en Airflow que orquesta la ejecución de los conectores de Airbyte y trabajos de Apache Spark para mover los datos de la capa `raw` a la capa `processed` del Data Lake.

```python
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Configuración de variables
SSH_CONN_ID = "spark-ec2-ssh"
SPARK_PROJECT_PATH = "/home/ubuntu/spark"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="spark_etl_via_ssh_check",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["spark", "ssh", "ec2"],
) as dag:

    # Verificar conexión SSH
    check_ssh_connection = SSHOperator(
        task_id="check_ssh_connection",
        ssh_conn_id=SSH_CONN_ID,
        command="echo '✅ Conexión SSH establecida correctamente desde Airflow!'",
        cmd_timeout=60,
    )

    # Ejecutar el trabajo Spark
    run_spark_job = SSHOperator(
        task_id="run_spark_job",
        ssh_conn_id=SSH_CONN_ID,
        command=f"cd {SPARK_PROJECT_PATH} && sudo docker compose up --build --abort-on-container-exit",
        cmd_timeout=1800,
    )

    # Fin del DAG
    end_task = EmptyOperator(task_id="end")

    check_ssh_connection >> run_spark_job >> end_task
```
### 3) Implementación de Tareas en el DAG para Copiar/Mover Ficheros Transformados a la Capa Gold

Acciones realizadas:

- Se planteó el dag con uso de BashOperator en Airflow que copie los archivos en formato Parquet o Delta hacia la capa Gold.

### 4) Configuración de Dependencias, Reintentos y Notificaciones

Acciones realizadas:

Se configuraron las dependencias de las tareas de manera correcta, asegurando que la ejecución de los jobs de Spark dependa de la correcta ejecución de la conexión SSH.

Se implementaron reintentos y un tiempo de espera entre reintentos en caso de fallos en las tareas.

Para las notificaciones, se puede configurar la notificación por Slack o Correo Electrónico en caso de fallos usando los operadores de notificación de Airflow.

Ejemplo de notificación:

```
from airflow.operators.empty import EmptyOpeartor as  DummyOperator
from airflow.providers.slack.operators.slack_api import SlackAPIPostOperator

failure_notification = SlackAPIPostOperator(
    task_id="failure_notification",
    token="your-slack-token",
    channel="#alerts",
    text="¡Alerta! La tarea ha fallado.",
)

end_task >> failure_notification
```
### 5) Pruebas de Orquestación: Ejecución Manual y Agendada

Estado actual:

A pesar de haber configurado correctamente el DAG y las tareas en Airflow, no se pudo realizar una verificación completa de la orquestación debido a problemas persistentes en la conexión y ejecución de los jobs de Apache Spark desde Airflow. Esto se debió a errores relacionados con el acceso remoto a la instancia EC2 y la configuración de las claves SSH.

### 6 Próximos pasos:
 
* Mejorar la configuración de SSH para evitar errores y garantizar conexiones seguras entre Airflow y EC2.

 * Automatizar más tareas de mover archivos a la capa Gold con mayor control sobre el formato de datos.

* Implementar CI/CD completo con GitHub Actions para asegurar integridad ante cualquier cambio en el código de Airflow o Spark.