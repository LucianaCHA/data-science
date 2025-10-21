## **Diseño general del pipeline ETLT a implementar**

### 1. **Descripción del pipeline ETLT**

El pipeline de datos propuesto sigue un enfoque **ETLT (Extract, Load, Transform, Load)**, adaptado a una arquitectura de Data Lake moderna sobre Amazon Web Services (AWS). Este modelo permite la **ingesta inicial de datos desde múltiples fuentes**, su **almacenamiento en estado crudo (raw)** dentro de Amazon S3, y su posterior **procesamiento distribuido** mediante Apache Spark. Finalmente, los datos transformados son cargados en estructuras analíticas listas para ser consumidas por usuarios de negocio o herramientas de inteligencia de negocio.

Este diseño promueve una arquitectura **escalable, modular y gobernada**, capaz de adaptarse a nuevos casos de uso a medida que crece el volumen y la diversidad de los datos en la organización.

---

### 2. **Flujo general del pipeline**

El pipeline se organiza conceptualmente en tres bloques principales:

__Ingesta__: Captura e ingesta de datos desde APIs, bases de datos y archivos mediante Airbyte y Spark hacia la capa Raw de S3.

__Gobernanza y transformación__: Limpieza, estandarización y catalogación de los datos en AWS Glue, junto con la gestión de permisos en Lake Formation. Aquí se construyen las capas Bronze, Silver y Gold (Analytics).

__Consumo__: Exposición de los datos curados para dashboards, análisis avanzado y modelos predictivos.

La ejecución y orquestación de estos procesos se gestionan mediante Apache Airflow, mientras que GitHub Actions automatiza la entrega continua (CI/CD) de DAGs y scripts de transformación hacia el entorno de producción.

1. **Extracción e ingesta (Extract & Load):**
   - Herramientas como **Airbyte** permitirán la extracción de datos desde bases de datos relacionales (por ejemplo, MySQL), APIs REST públicas o privadas, y archivos planos (CSV, JSON).
   - Para la extracción en tiempo real (IoT, consumo de apis) se aplicará Kafka.
   - Los datos son cargados sin transformación previa en la **capa raw** del Data Lake (S3), preservando su estructura original para garantizar trazabilidad.

2. **Transformación (Transform):**
   - A través de **Apache Spark** y/o AWS Glue, se procesan los datos desde la capa raw hacia la **capa processed**, aplicando dos pasos:
    - Capa Bronce:
     - - Limpieza de datos inconsistentes.
     - - Estandarización de tipos y formatos.
     - - Detección de duplicados.
    - Capa Silver:
     - - Unión entre datasets relacionados (por ejemplo, ventas con productos o clientes).
     - - Enriquecimiento con datos externos (como clima o tráfico).
   - Los datos son almacenados en formato **Parquet o Delta Lake**, particionados por fecha u otras dimensiones relevantes.

3. **Carga final (Load to Gold):**
   - Los datos transformados y enriquecidos se consolidan en la **capa gold**, donde se calculan **KPIs y métricas de negocio**, y se generan tablas optimizadas para consultas analíticas.
   - Estas tablas se orientan a ser consumidas por analistas, científicos de datos o dashboards BI.

4. **Orquestación:**
   - Todo el flujo será orquestado mediante **Apache Airflow**, que permitirá:
     - Automatizar la ejecución de tareas (DAGs).
     - Gestionar dependencias, reintentos y logs.
     - Ejecutar pipelines de forma manual o agendada.

5. **Automatización (CI/CD):**
   - Se empleará **GitHub Actions** para automatizar flujos de CI/CD relacionados con:
     - Validación de código.
     - Despliegue de scripts de transformación.
     - Publicación de DAGs en el entorno de Airflow.

---

### 3. **Objetivos clave del pipeline**

- Garantizar la **integración eficiente de múltiples fuentes de datos**.
- Asegurar la **calidad, trazabilidad y gobernanza de los datos** mediante el uso de Lake Formation y una arquitectura en capas.
- Facilitar el **análisis exploratorio y predictivo** gracias a una capa gold optimizada.
- Promover la **automatización y mantenibilidad** del flujo de datos en el tiempo.

---

### 4. **Diagrama de arquitectura**

Se incluye el **diagrama de arquitectura** donde se representen las siguientes etapas:

- **Fuentes de datos:** Bases de datos, APIs, sensores IoT, scraping, archivos planos.
- **Herramienta de ingesta:** Airbyte.
- **Almacenamiento en Data Lake:** S3, organizado por capas (`raw`, `processed`, `gold`).
- **Transformación distribuida:** Apache Spark en PySpark.
- **Orquestación de flujos:** Apache Airflow.
- **Automatización y control de versiones:** GitHub + GitHub Actions.
- **Gobernanza y permisos:** AWS Lake Formation.

![diagrama](/pi_mod_04/assets/eltl_diagram.svg)



[`eltl_diagram`](./assets/eltl_diagram.svg)
[Acceso online al diagrama para comentar](https://lucid.app/lucidchart/c91b55ea-7559-49a4-8571-d07b4a7a1002/edit?viewport_loc=-4931%2C-2203%2C3531%2C1317%2C0_0&invitationId=inv_8b2c5398-513b-442c-8c6a-c34ba0b6cdf3)


---
---


## **Definición y Propósito de las Capas del Data Lake**

### 1. **Introducción a la Estructura por Capas**

Para garantizar una arquitectura escalable, gobernable y mantenible, se ha definido una estructura por capas dentro del Data Lake alojado en Amazon S3. Esta estructura se alinea con los principios modernos de arquitectura de datos, separando claramente las fases de ingestión, procesamiento y consumo. Cada capa cumple un rol específico dentro del pipeline ELT, facilitando la trazabilidad, reutilización y gobernanza de los datos.

---

### 2. **Capas del Data Lake**

#### **Capa Raw**

* **Propósito:**
    Almacenar los datos exactamente como se reciben de las fuentes originales, sin ninguna transformación, limpieza o enriquecimiento. Esta capa actúa como respaldo seguro y referencia de auditoría para todo el pipeline.

* **Características:**
    * Datos en formatos originales (CSV, JSON, Avro, etc.).
    * Organizados por fuente y tipo de dato.
    * Incluye datos transaccionales, interacciones de clientes, registros de sensores y fuentes externas.
    * Los esquemas pueden ser semiestructurados o no estructurados.

* **Ejemplo de contenidos:**
    * Transacciones extraídas de MySQL o APIs.
    * Registros de soporte al cliente o datos de navegación.
    * Datos brutos de sensores (temperatura, GPS, humedad).
    * Datos externos como clima o precios de la competencia (vía scraping/API).

* **Estructura implementada:**

```plaintext
s3://lucianacha-pi-mod4/
└── raw/
        ├── transactions/
        │   ├── from_db/
        │   ├── from_api/
        │   └── from_csv/
        │
        ├── customers/
        │   ├── support_tickets/
        │   └── navigation_logs/
        │
        ├── sensors/
        │   ├── temperature/
        │   └── gps_tracking/
        │
        ├── external/
        │   ├── traffic_api/
        │   └── weather_api/
        |       ├── forecast/         <-- proceso de Airbyte diario
        │              └── city
        |                   └── city=xxx/year=YYYY/month=MM/day=DD/...
        |       └── historical/
        |           └── city
        |                 └── city=xxx/year=YYYY/month=MM/day=DD/...
        │
        └── metadata/
                ├── ingestion_logs/
                └── data_schemas/
```

#### **Capa Processed**

* **Propósito:**
    Almacenar datos que han sido limpiados, transformados y estandarizados — listos para integración, enriquecimiento o aplicación de lógica de negocio. Esta capa incluye validación, formateo, normalización y uniones de conjuntos de datos.

* **Características:**
    * Datos estructurados en formatos eficientes como Parquet o Delta Lake.
    * Estructura tabular compatible con motores analíticos.
    * Transformaciones aplicadas usando Apache Spark o SQL.
    * Organizados con particiones temporales (year=2025/month=09, etc.).

* **Ejemplo de contenidos:**
    * Datos de ventas limpios con tipos consistentes.
    * Registros de clientes deduplicados y normalizados.
    * Datos de sensores combinados con ubicación y marcas de tiempo.
    * Enriquecimiento por datos derivados:
        is_extreme_weather: booleano si hay condiciones de alerta.

* **Estructura implementada:**

```plaintext
s3://lucianacha-pi-mod4/
└── processed/
        ├── sales/
        │   ├── consolidated/
        │
        ├── customers/
        │   ├── summarized_transactions/
        │
        ├── products/
        │   ├── enriched_db_with_api/
        │
        ├── sensors/
        │   ├── normalized_temperature/
        │   ├── normalized_gps/
        │   ├── normalized_weather/
        │   └── daily_summary/
        │
        ├── dim_time/
        │   └──year=2025/
        │   └── daily_summary/
```

Los datos periódicos se particionan por fecha siguiendo el esquema:
processed/sales/consolidated/year=2025/month=09/day=30/

---

#### **Capa Gold**

* **Propósito:**
    Almacenar conjuntos de datos listos para análisis de negocio, reportes, modelos de machine learning o dashboards de BI. Esta capa contiene datos curados, KPIs, métricas agregadas y tablas diseñadas para consumo directo.

* **Características:**
    * Datos altamente estructurados y optimizados para consumo.
    * Puede particionarse por dimensiones clave (ej: fecha, región, producto).
    * Curados y validados según reglas de negocio.
    * Expuestos al Data Warehouse o herramientas de BI.

* **Ejemplo de contenidos:**
    * KPIs de ventas mensuales por canal.
    * Probabilidades de churn de clientes.
    * Métricas operativas basadas en el desempeño de sensores.
    Indicadores agregados por ciudad, día, semana:


* **Estructura implementada:**

```plaintext
s3://lucianacha-pi-mod4/
└── gold/
        ├── kpi_sales/
        │   ├── monthly_sales/
        │   ├── sales_by_channel/
        │   └── top_products/
        │
        ├── customers/
        │   ├── frequent_customers/
        │   ├── churn_probability/
        │
        ├── operational_status/
        │   ├── sensor_anomalies/
        │   ├── at_risk_inventory/
        │   └── logistics_summary/
        │
        ├── external_indicators/
        │   ├── weather_sales_correlation/
        │   ├── weather_daily_summary/
        │       └── weather_daily_summary/
        |           └── city=Patagonia/year=2025/month=09s_summary/
        |           └── city=Patagonia/year=2025/month=08s_summary/
```

---

### 3. Ventajas de la Organización por Capas

* **Modularidad:** Permite escalar y evolucionar cada etapa del pipeline de forma independiente.
* **Trazabilidad:** Permite reconstruir cualquier capa a partir de la anterior.
* **Gobernanza:** Facilita la gestión de permisos y el linaje de datos usando herramientas como AWS Lake Formation.
* **Performance:** El uso de formatos columnares en las capas processed y gold mejora la eficiencia de las consultas y reduce costos.

---

### 4. Selección y Justificación del Stack Tecnológico

El stack tecnológico fue seleccionado en función de los requerimientos de escalabilidad, integración, rendimiento y gobernanza de cara a un negocio en constante crecimiento.


| Componente                    | Tecnología                  | Justificación                                                                                            |
| ----------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Almacenamiento**            | **Amazon S3**               | Servicio altamente escalable y económico. Base del Data Lake.                                            |
| **Gobernanza y permisos**     | **AWS Lake Formation**      | Permite definir políticas de acceso centralizadas y catálogos de datos.                                  |
| **Ingesta**                   | **Airbyte**                 | Conectores nativos para bases relacionales, APIs y archivos. Facilita la automatización de extracciones. |
| **Transformación**            | **Apache Spark (PySpark)**  | Procesamiento distribuido para grandes volúmenes de datos. Compatible con Delta Lake.                    |
| **Orquestación**              | **Apache Airflow**          | Control total de dependencias, reintentos, logging y ejecución programada.                               |
| **Versionado y CI/CD**        | **GitHub + GitHub Actions** | Integración continua para validar y desplegar scripts y DAGs.                                            |
| **Formato de almacenamiento** | **Parquet / Delta Lake**    | Eficiencia en lectura, compresión y manejo de actualizaciones.                                           |

---

### 5. Identificación y Análisis de las Fuentes de Datos

La organización integrará información desde diversas fuentes, con el objetivo de responder preguntas clave del negocio, al momento de esta entrega se desconoce tipo de negocio pero se cuenta con datos de una Api de climaÇ; con lo cual se presupone un negocio tipo retail, multicanal , con logistica propia para el manejo de preguntas de negocio:

* ¿Qué factores externos influyen en el rendimiento de ventas?
* ¿Cómo varía el comportamiento de los clientes según la región o el clima?
* ¿Qué patrones se observan en el desempeño de sensores o procesos operativos?


| Fuente                                                   | Tipo             | Descripción                                     | Relevancia Analítica                                       |
| -------------------------------------------------------- | ---------------- | ----------------------------------------------- | ---------------------------------------------------------- |
| **Base de datos MySQL (transacciones)**                  | Relacional       | Ventas, productos, clientes.                    | Permite construir KPIs y modelos de predicción de demanda. |
| **APIs externas (clima, tráfico, precios competidores)** | API REST         | Datos externos para enriquecimiento contextual. | Relacionar condiciones externas con resultados de negocio. |
| **Archivos CSV / JSON (reportes operativos)**            | Archivo plano    | Datos generados por áreas internas.             | Integración rápida y análisis histórico.                   |
| **Datos de sensores IoT**                                | Streaming / Logs | Monitoreo ambiental o de procesos.              | Identificación de anomalías o correlaciones con ventas.    |


### 6. Preguntas de negocio y mapeo a fuentes

| **Pregunta de negocio**                                                                                  | **Fuentes de datos requeridas**                                   | **Valor analítico / Objetivo**                                            |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------- |
| ¿En qué días y horarios se concentran la mayor cantidad de ventas por ciudad y canal?                    | Ventas por timestamp, ciudad, canal                               | Optimizar horarios de apertura, staffing y campañas por franja horaria    |
| ¿Cuáles son las temporadas de mayor venta por categoría y cómo varían año a año?                         | Ventas históricas por categoría y fecha, calendario               | Planificación de compras, forecasting estacional, campañas anticipadas    |
| ¿Qué productos muestran mayor sensibilidad estacional?                                                   | Ventas históricas por producto                                    | Identificar productos para planificación especial (pre-stocking)          |
| ¿Qué campañas o promociones tienen mejor rendimiento bajo determinadas condiciones climáticas?           | Promociones, ventas por producto, clima                           | Optimizar inversión en marketing y seleccionar ofertas por contexto       |
| ¿Qué productos tienen alta rotación en ciertas temporadas y baja en otras?                               | Ventas por timestamp                                              | Optimizar plan de ofertas por temporadas                                  |                 
| ¿Cuál es el tiempo medio hasta reposición de stock en zonas con diferentes condiciones climáticas?       | Inventario, tiempos de reabastecimiento, clima                    | Definir buffers de stock y políticas de reorder por región                |
| ¿Cómo varían las tasas de conversión online cuando el clima impacta tráfico en tienda física?            | Ventas online, visitas web, afluencia tiendas físicas, clima      | Planificar promociones omnicanal y medir cannibalización entre canales    |
| ¿Qué impacto tiene la estacionalidad climática en la retención de clientes?                              | Cohortes de clientes, compras recurrentes, clima                  | Diseñar acciones de retención en periodos críticos                        |
| Hay relación en la combinación de productos funcionan según clima (cross-sel)?                           | Ventas por transacción (líneas), clima                            | Mejorar recomendaciones y promociones contextuales                        |
| ¿Qué regiones deberían priorizar envíos acelerados o seguros por fenómenos meteorológicos frecuentes?    | Historial de demoras logísticas, rutas, clima                     | Optimizar rutas, logística preventiva .                                   |
| ¿Qué productos requieren packaging o almacenaje especial por alta humedad/temperatura?                   | Devoluciones/daños por producto, condiciones de almacenaje, clima | Reducir pérdidas, mejorar calidad de inventario y decisiones de packaging |
| ¿Se reducen las ventas en locales físicos si la probabilidad de lluvia supera Y%? Aumenta ecommerce?     | Ventas tienda física y online, clima por ciudad                   | Ajustar estrategias omnicanal y campañas de marketing digital             |
| ¿Qué canales de venta (online, tienda física) presentan mayor conversión según condiciones externas?     | Ventas online, visitas web, afluencia tiendas físicas, clima      | Optimizar rutas y planificar buffers de entrega                           |
| ¿Qué zonas muestran mayor correlación entre vientos fuertes y demoras logísticas?                        | Logística (tiempos de entrega), clima por ruta/ciudad             | Optimizar rutas y planificar buffers de entrega                           |


---

### Conclusión

Este primer avance del proyecto ha permitido sentar las bases de un Data Lake moderno, escalable y gobernado, aplicando conceptos clave de arquitectura de datos en la nube, ETLT y gobernanza con Lake Formation. La definición de la estructura en capas, la selección del stack tecnológico y el mapeo de fuentes de datos a preguntas de negocio ha facilitado comprender cómo los datos pueden transformarse en información útil para la toma de decisiones.

Desde el punto de vista académico, esta etapa ha sido fundamental para consolidar conocimientos prácticos en ingesta de datos, procesamiento distribuido, orquestación de pipelines y modelado de datos, integrando teoría y práctican. Además, permitió entender la importancia de la trazabilidad, la gobernanza y la planificación de un flujo de datos eficiente pensando en un caso de uso real.