1. [Descripción General](#descripción-general)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Modelo de datos](#modelo-de-datos)
4. [Configuración y Ejecución](#configuración-y-ejecución)
  - [Requisitos](#1-requisitos)
  - [Construcción y ejecución](#2-construcción-y-ejecución)
  - [Transformaciones Implementadas](#3-transformaciones-implementadas)
  - [Trabajando con EC2](#4-trabajando-con-ec2)
5.  [Consideraciones y Buenas Prácticas](#5-consideraciones-y-buenas-prácticas)
6.  [Próximos Pasos](#6-próximos-pasos)
7. [Referencias Técnicas](#referencias-técnicas)
## Descripción General

Este proyecto tiene como objetivo procesar datos climáticos **históricos y diarios** provenientes de archivos JSON y Parquet utilizando **PySpark**, normalizarlos y almacenarlos en formato **Parquet particionado** en una capa `processed` dentro de un Data Lake en **Amazon S3**.

Se busca:
- Unificar estructuras entre distintos orígenes de datos.
- Normalizar y enriquecer la información meteorológica.
- Optimizar los datos para análisis posteriores (por ciudad y fecha).
- Preparar el pipeline para orquestación con Apache Airflow.

El entorno está montado con **Docker Compose**, ejecutado y probado en una **instancia EC2** de AWS.

Todo el código necesario se encuentra en [spark](/pi_mod_04/delivery/03-third-delivery/spark_project/). El pipeline fue pensado para obtener de forma optima datos de clima por fecha y ciudad para ser utilizados en analisis de ventas (còmo afecta el clima a as ventas por tal ocula canal, como afecta el clima a la logistica, el modelo de datos busca dar eficiencia para cosultas por fecha/ ciudad y algunos flasgs como is_cloudy)

---

## Estructura del Proyecto

```
spark_project/
├── app/
│ ├── scripts/
│ │ └── spark/
│ │ ├── transform_historical.py # Procesamiento de históricos
│ │ ├── transform_dailies.py # Procesamiento de pronósticos
│ │ └── init.sh # Script de ejecución automatizada
│ └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Modelo de datos

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

---

## Configuración y Ejecución

### 1. Requisitos

  - Docker
  - Acceso a S3 vía InstanceProfile (EC2) o credenciales
  - IAM Role con permisos sobre los buckets
  - Renombrar archivo env.example como .env y reemplazar credenciales aws

---

### 2. Construcción y ejecución

```bash
docker-compose up --build
```

### 3. Transformaciones Implementadas

#### `transform_historical.py`

* Lee JSON desde S3 (historical/).
* Extrae y transforma campos como fecha, temperatura, ciudad, clima, etc.
* Convierte a formato Parquet particionado por city y date.
* Modo de escritura: overwrite (reemplaza la partición).

#### `transform_dailies.py`

- Lee datos diarios (forecast) en formato Parquet con búsqueda recursiva.
- Extrae la ciudad desde el path del archivo.
- Explota la lista de pronósticos por día.
- Normaliza campos y crea columnas útiles (como flags de lluvia o nublado).
- Escribe datos particionados por `city` y `date` en la capa processed.
- Modo de escritura: `append` (agrega nuevos datos sin borrar existentes).

#### `run_jobs.sh`

- Script bash que ejecuta secuencialmente los scripts PySpark.
- Facilita la orquestación dentro del contenedor `init`.

---


### 4. Trabajando con EC2

1. Conexión a instancia:

```bash
chmod 400 pi-mod4.pem
ssh -i "pi-mod4.pem" ubuntu@<EC2-PUBLIC-IP>
```

2. Instalación de Docker:

```
sudo apt update && sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

3.Subida del proyecto y ejecución:
```
scp -r spark_project/ ubuntu@<EC2-PUBLIC-IP>:/home/ubuntu/
cd spark_project
docker-compose up --build

```

4. Resultado:

- Transformaciones exitosas.

- Datos escritos en S3, verificados desde la consola.

- Spark UI accesible desde EC2 vía tunel SSH si se desea.

### 5. Consideraciones y Buenas Prácticas

Los datos están particionados por ciudad y fecha para optimizar consultas y escrituras.

El procesamiento incremental debe manejarse mediante control de archivos ya procesados, para evitar duplicados.

Se recomienda implementar un mecanismo de tracking (tabla o archivo de control) para optimizar re-procesos.

Cachear DataFrames cuando se reutilizan para mejorar el rendimiento, cuidando el uso de memoria.

Validar la correcta configuración de credenciales y acceso a S3 para lectura/escritura.

### 6. Próximos Pasos

Integrar mecanismo de tracking para evitar duplicación de datos.

Agregar caching en los scripts PySpark para optimización.

Desplegar el procesamiento con Apache Airflow para orquestación programada.

Mejorar manejo de errores y logging para facilitar monitoreo.

### Referencias Técnicas

Apache Spark: https://spark.apache.org/docs/latest/

PySpark API: https://spark.apache.org/docs/latest/api/python/index.html

AWS S3 + Spark: https://hadoop.apache.org/docs/r3.3.2/hadoop-aws/tools/hadoop-aws/index.html