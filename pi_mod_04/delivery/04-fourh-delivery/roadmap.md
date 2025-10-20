sobre esta consigna Implementación de tareas en el DAG para copiar o mover ficheros transformados hacia la capa gold, incluyendo particionamiento y formato Parquet/Delta. tengo dudas . hoy los datos que se guradan crudis son loa diarios del clima (airbuyte) y un jsn de historicos. Con spark se normaliza ambas fuentes a un unico modelo y se guardan particionados por dia/ciudad pensando en que quedncomodos para analiticia  ## Modelo de datos

| Campo        | Tipo      | Descripción                     |
| ------------ | --------- | ------------------------------- |
| city         | string    | Ciudad normalizada (minúsculas) |
| datetime     | timestamp | Fecha y hora completa           |
| date         | date      | Solo fecha                      |
| temperature  | float     | Temperatura                     |
| humidity     | int       | Humedad                         |
| weather_main | string    | Tipo de clima (Rain, Clouds...) |
| is_rainy     | boolean   | Indicador si llueve             |
| is_cloudy    | boolean   | Indicador si está nublado       |
| wind_speed   | float     | Velocidad del viento            |
| wind_deg     | float     | Dirección del viento            |

 esto quedo asi porque no hay datos de ventas y es un proyecto academico . con lo cual mi planteo fue pensar preguntas que traten de evaluar como afecta  l clima a la logistica / ventas de ahi que seplanteo este modelo. Nosé que podria plantear como capa gold en este contexto



from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

# Example failure notification callback
def send_failure_notification(context):
    # Here you can customize to send a message to Slack, email, etc.
    # context will give you info on the failed task
    print(f"Task failed: {context['task_instance'].task_id}")



SparkSubmitOperator: Este operador es utilizado para ejecutar trabajos de Spark, usando spark-submit.

application: Este parámetro apunta al archivo de script Spark que quieres ejecutar (debe estar accesible desde el contenedor de Airflow).

conn_id: Es la conexión de Airflow que define cómo se conecta Airflow a tu clúster Spark. Este debe ser configurado en la UI de Airflow o en el archivo airflow.cfg.

conf y otros parámetros: Puedes ajustar la configuración de Spark según lo que necesites (memoria, núcleos, etc.).

Configurar la conexión de Spark en Airflow:

Antes de ejecutar el DAG, debes asegurarte de que Airflow tenga una conexión válida a tu clúster de Spark. Esto se hace configurando una conexión Spark en la UI de Airflow.

Abre la UI de Airflow (http://localhost:8080 si usas el docker-compose por defecto).

Ve a la sección de Admin > Connections.

Agrega una nueva conexión con el siguiente formato:

Conn Id: spark_default (o el nombre que utilices en el DAG).

Conn Type: Spark. (no existe en imagen base, instalar pip install apache-airflow-providers-apache-spark
)

Host: La dirección de tu servidor Spark (por ejemplo, spark://<IP_DEL_CLUSTER>:7077 si usas el modo standalone o el nombre del servicio si usas Docker).

Port: 7077 (por defecto).

Configura el resto de campos si es necesario (si usas autenticación, etc.).