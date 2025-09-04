# Entregable 2: Data Pipeline - Capa Raw

---
Este proyecto automatiza la extracción, carga y validación de datos de *Airbnb*, almacenándolos en la capa raw en *Google Cloud Storage y PostgreSQL*. Además, genera reportes de calidad y coherencia en JSON y HTML.
--



## 1. Requisitos

- Python ≥ 3.10

- Docker

- Google Cloud SDK (gcloud) configurado

- Acceso al bucket de GCS y a la instancia de PostgreSQL

- Variables de entorno definidas (opcional, se pueden usar defaults en Settings)

---

## 2. Configuración

Las configuraciones se manejan con la clase Settings y pueden definirse como variables de entorno:

| Variable        | Default          | Descripción                    |
| --------------- | ---------------- | ------------------------------ |
| `DB_HOST`       | database         | Host de PostgreSQL             |
| `DB_PORT`       | 5432             | Puerto de PostgreSQL           |
| `DB_NAME`       | NOT_SET          | Nombre de la base de datos     |
| `DB_USER`       | NOT_SET          | Usuario                        |
| `DB_PASSWORD`   | NOT_SET          | Contraseña                     |
| `GCS_BUCKET`    | NOT_SET          | Bucket de Google Cloud Storage |
| `GCS_FILE_PATH` | raw/data/airbnb/ | Prefijo de los CSV en GCS      |

    - Nota: DB_URL se construye automáticamente para conectarse a PostgreSQL (incluso con Cloud SQL).

### Ejecución local (con Docker)

1. Construir la imagen:

```bash
docker build -t airbnb-pipeline:latest .

```

2. Ejecutar la imagen:

```bash
docker run --rm \
    -e DB_HOST=<POSTGRES_HOST> \
    -e DB_USER=<POSTGRES_USER> \
    -e DB_PASSWORD=<POSTGRES_PASSWORD> \
    -e GCS_BUCKET=<BUCKET_NAME> \
    airbnb-pipeline:latest
```

    - Esto:

        Descarga los CSV del bucket configurado.

        Crea la tabla airbnb_raw en PostgreSQL si no existe.

        Valida los datos (calidad, completitud, coherencia).

        Carga los datos a PostgreSQL.

        Genera reportes JSON y HTML en reports/ y reports_html/ dentro del bucket.

### Ejecución en Google Cloud Run

* Subir la imagen a Google Container Registry (GCR) o Artifact Registry:

```bash
docker tag airbnb-pipeline:latest gcr.io/<PROJECT_ID>/airbnb-pipeline:latest
docker push gcr.io/<PROJECT_ID>/airbnb-pipeline:latest
```
* Despliegue en Google run 

```bash
gcloud run deploy airbnb-pipeline \
    --image gcr.io/<PROJECT_ID>/airbnb-pipeline:latest \
    --platform managed \
    --region <REGION> \
    --allow-unauthenticated \
    --set-env-vars DB_HOST=<POSTGRES_HOST>,DB_USER=<POSTGRES_USER>,DB_PASSWORD=<POSTGRES_PASSWORD>,GCS_BUCKET=<BUCKET_NAME>
```



### Estructura de reportes

JSON: reports/<archivo>_<timestamp>.json
Contiene todas las métricas de validación.

HTML: reports_html/<archivo>_<timestamp>.html
Reporte visual de validación (columnas faltantes, nulos, tipos, duplicados y coherencia).

Los reportes HTML se pueden desplegar en un endpoint de FastAPI o abrir directamente desde el bucket.


---

### Pipeline resumido

- Descarga los CSV desde GC y los cataloga con nombre versionado en directorio adecuado.

- Descarga consulta de cotizaciónes de dolar en formato json y nomenclado en directorio adecuado.

- Valida completitud, calidad y coherencia de datos de alquileres (csv)

- Carga los datos en PostgreSQL (airbnb_raw), previa validaciones minimas.

- Genera reportes JSON y HTML y los sube a GCS.

---

### Conclusión

Se implementó un pipeline automatizado de extracción y carga de datos de Airbnb hacia la capa raw en Google Cloud, cumpliendo con los requerimientos de la consigna:

__Extracción confiable__: los archivos CSV se descargan directamente desde un bucket de GCS y se cargan en un DataFrame de Pandas.

__Validación de datos__: se realiza un análisis completo de calidad (tipos de datos, nulos, duplicados), completitud (columnas esperadas) y coherencia (valores geográficos y precios).

__Almacenamiento estructurado__: los datos se guardan en una tabla airbnb_raw en PostgreSQL, preservando el valor analítico para transformaciones futuras.

__Reportes automáticos__: se generan reportes en JSON y HTML, que documentan el estado de los datos y pueden visualizarse fácilmente.

__Contenerización y despliegue en la nube__: el pipeline fue preparado como imagen Docker optimizada para Google Cloud, permitiendo ejecución reproducible en Cloud Run.

__Acceso y trazabilidad__: se puede acceder al pipeline desplegado en [Google Cloud Run](https://pi-mod03-data-ingestion-314936653450.us-central1.run.app/)
 y a la imagen Docker en [Docker Hub](https://hub.docker.com/repository/docker/lucianacha/pi-mod03-data-ingestion/tags/latest/sha256-f4a50ec001141942cc2e79d313cbbb67503ee138c0c66ce5cfddf552cbf8eb95)
.

__Visión futura__: se planea incorporar endpoints para carga manual de datos, facilitando el uso por usuarios no técnicos, y automatizar el despliegue completo del pipeline.
A nivel técnico se plantea la necesidad de mejora en el manejo de variables de entorno, por ej DB conection , user y passwords de base de  datos deben ir como secrets sin embargo por cuestiones de tiempo en adquirir conocimiento para implementar despliegue en run y demas no se realizó.

Esta implementación asegura que la integración de datos sea fiable, reutilizable y alineada con los objetivos de negocio, sentando una base sólida para futuras transformaciones y análisis.