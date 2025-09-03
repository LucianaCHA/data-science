### **1. Roadmap de Desarrollo:**

#### **Fase 1: Definir el Flujo de Recolección de Datos**

**Objetivo:** Crear el script para la extracción de datos desde APIs, asegurando que se estructuren correctamente en un formato adecuado.

1. **Recolección de Datos desde APIs:**

   * Usar librerías como `requests` o `httpx` para interactuar con APIs.
   * Parámetrizaremos los endpoints y los parámetros (por ejemplo, API keys, parámetros de fecha, etc.).
   * Manejo de errores (reintentos, fallos de conexión) y control de respuestas (200 OK, 500 Internal Server Error, etc.).

2. **Recolección de Datos por Web Scraping:**

   * Usar `BeautifulSoup` o `Selenium` para scrapear sitios web.
   * Implementar técnicas como el manejo de tiempo de espera o la paginación.
   * Asegurarse de que los datos se guarden de forma estructurada (JSON, CSV) para un procesamiento posterior.

3. **Almacenaje Local:**

   * Guardar los datos en estructuras adecuadas como `DataFrame` (Pandas) o en archivos `.json`, `.csv` según el tipo de datos extraídos.
   * Asegurarse de que los datos sean guardados en la carpeta `raw` en el formato adecuado.

4. **Contenerización con Docker:**

   * Crear un `Dockerfile` que contenga el script de recolección de datos y sus dependencias.
   * Validar que la imagen se construya y se ejecute correctamente usando `docker build` y `docker run`.

---

#### **Fase 2: Validación y Estructuración de los Datos**

**Objetivo:** Validar la calidad, completitud y coherencia de los datos, luego estructurarlos en un formato estándar (CSV, JSON).

1. **Verificación de Carga:**

   * Implementar un script para verificar que los archivos fueron almacenados correctamente (comprobación de existencia, tamaño, integridad).
   * Enviar alertas o generar logs en caso de fallos en la carga.

2. **Estandarización de Formatos:**

   * Convertir los datos a formatos estándar según el tipo (CSV, JSON).
   * Nombrar los archivos de forma coherente con la convención de nombres (`fuente-tipo-frecuencia de extracción.extension`).

3. **Validación de Calidad de Datos:**

   * Crear una rutina que valide:

     * **Calidad**: Tipos correctos de datos, valores nulos.
     * **Completitud**: Todos los campos requeridos están presentes.
     * **Coherencia**: Asegurarse de que no haya inconsistencias (fechas válidas, números positivos).
   * Generar reportes de validación y almacenarlos.

---

#### **Fase 3: Contenerización y Despliegue en la Nube**

**Objetivo:** Crear una imagen Docker que se pueda desplegar en Google Cloud y que facilite la automatización del pipeline.

1. **Dockerización del Script:**

   * Crear un `Dockerfile` que:

     * Use `python:3.10-slim` como imagen base.
     * Instale las dependencias necesarias desde un archivo `requirements.txt`.
     * Defina un `ENTRYPOINT` claro para ejecutar el script.

2. **Subida de la Imagen Docker a un Repositorio:**

   * Subir la imagen a registro de contenedores **Google Artifact Registry**.
   * Definir una convención de nombres para las versiones de la imagen Docker.

3. **Implementación de CI/CD con GitHub Actions:**

   * Crear un flujo básico en **GitHub Actions** para construir y desplegar la imagen Docker a Google Cloud (o cualquier plataforma elegida).
   * Validar que la integración con Google Cloud esté funcionando correctamente (despliegue de contenedores).

---

#### **Fase 4: Integración con el Pipeline ELT**

**Objetivo:** Integrar este proceso de recolección de datos con el pipeline ELT (Extract, Load, Transform).

1. **Integración con Data Warehouse:**

   * Conectar el proceso de extracción de datos con el almacenamiento de datos en la capa **Raw** de tu Data Warehouse.
   * Aplicar transformaciones mínimas para garantizar la coherencia y calidad de los datos.

2. **Orquestación con Airflow o Prefect:**

   * Crear un DAG (Directed Acyclic Graph) en **Apache Airflow** o **Prefect** para automatizar la ejecución de los scripts de extracción.
   * Validar que el proceso de recolección, carga y transformación se ejecute sin problemas en un entorno en la nube.

---

### **2. Estructura de Archivos:**

```plaintext
pi_3/
│
│
├── app/
|   ├── api/ # endpoints si fuesen necesarios
    │
│   ├── __init__.py                  # Inicialización del módulo
│   ├── assets/                      # Imágenes y recursos estáticos
│   ├── config/
│   │   └── config.py                # Clase para obtener configuraciones del entorno
│   ├── db/
│   │   ├── base.py                  # Modelo base para SQLAlchemy
│   │   └── session.py               # Conexión a la base de datos (SQLAlchemy)
│   ├── models/                      # Modelos de la base de datos
│   ├── repository/                  # Acceso a datos
│   ├── services/                    # Lógica de negocio
│   ├── utils/                       # Funciones utilitarias
│   ├── storage_handler.py           # Manejo y validación de almacenamiento
│
├── dbt_project/                     # Proyecto DBT (transformación de datos)
│
├── delivery/
│   ├── first/                       # Directorio de entregables
│   ├── second/    
│   ├── third
│
├── scripts/
│   ├── db/                          # Scripts de base de datos (migraciones, inicialización)
│   ├── data/                        # Archivos de datos (CSV, etc.)
│   ├── init.sh                      # Script de inicialización
│   └── loader/
│       └── load_all.py              # Carga de datos a la base (invoca repo/services)
│
├── Dockerfile                       # Contenerización del proceso
├── docker-compose.yml               # Orquestación de servicios
├── .env                             # Variables de entorno
├── .github/
│   └── workflows/
│       └── ci_cd.yml                # CI/CD con GitHub Actions
└── README.md                        # Documentación del proyecto
```