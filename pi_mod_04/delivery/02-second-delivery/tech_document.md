# Documentación técnica - Integración Airbyte: OpenWeatherMap → S3 (Parquet)

## Descripción General

Se implementó una integración de datos utilizando **Airbyte 7.3.0**, extrayendo información meteorológica desde la API pública de **OpenWeatherMap** y almacenándola en **Amazon S3** en formato **Parquet**, siguiendo una estructura jerárquica pensada para futuras consultas con Athena o cargas a un data lake.

---

## Fuente de Datos (Source)

[documento airbyte source](/pi_mod_04/delivery/02-second-delivery/weather_api_patagonia.yaml)

- **Tipo de conector:** `DeclarativeSource`
- **Nombre del stream:** `weather_api`
- **API consumida:** `https://api.openweathermap.org/data/2.5/forecast`

### Parámetros de consulta:

| Parámetro | Valor              |
| --------- | ------------------ |
| `lat`     | -41.810147         |
| `lon`     | -68.906269         |
| `cnt`     | 8 (registros)      |
| `appid`   | `{API_KEY}`        |
| `units`   | metric             |

- **Método HTTP:** `GET`
- **Formato de respuesta:** JSON
- **Extractor:** `DpathExtractor` (campo raíz `[]` para todo el objeto)

### Esquema de datos extraídos

Incluye:

- Tiempo (`dt`, `dt_txt`)
- Condiciones principales (`temp`, `feels_like`, `humidity`, etc.)
- Detalles climáticos (`weather`, `wind`, `visibility`, `pop`, etc.)
- Datos de ubicación (`city`, `coord`, `country`, etc.)

| Campo                   | Tipo    | Descripción                                      |
|-------------------------|---------|--------------------------------------------------|
| `dt`                    | number  | Timestamp                      |
| `dt_txt`                | string  | Fecha y hora del pronóstico (`YYYY-MM-DD HH:MM`) |
| `main.temp`             | number  | Temperatura (°C)                                 |
| `main.feels_like`       | number  | Sensación térmica                                |
| `main.humidity`         | number  | Humedad (%)                                      |
| `weather[].main`        | string  | Condición principal (ej: Clear, Rain)            |
| `weather[].description` | string  | Descripción textual del clima                    |
| `wind.speed`            | number  | Velocidad del viento (m/s)                       |
| `visibility`            | number  | Visibilidad (metros)                             |
| `pop`                   | number  | Probabilidad de precipitación (0 a 1)            |
| `city.name`             | string  | Ciudad                                           |
| `city.country`          | string  | País                                             |

### Frecuencia de sincronización

- **Modo:** 24 hs, manual.
- **Justificación:** Límite de sincronizaciones del Free Tier de Airbyte
---

## Esquema del Destino (Destination)
[json destination](/pi_mod_04/delivery/02-second-delivery/json-output-airbyte.json)


- **Destino:** Amazon S3
- **Nombre del destino:** `S3-lucianacha-pi-mod4`
- **Bucket:** `lucianacha-pi-mod4`
- **Ruta base:** `raw/external_data/`
- **Formato de archivo:** `Parquet` (con compresión `Snappy`)

### Parámetros del formato:

```json
{
  "format_type": "Parquet",
  "compression_codec": "SNAPPY",
  "page_size_kb": 1024,
  "block_size_mb": 128,
  "dictionary_page_size_kb": 1024,
  "max_padding_size_mb": 8
}
ç

```
---
## Organización de archivos en S3

Los archivos Parquet se almacenan bajo:
__s3://lucianacha-pi-mod4/raw/external_data/weather_api/__

El nombre del archivo incluye un timestamp único generado por Airbyte

Este patrón permite el particionado futuro del bucket por fecha, ejemplo:

    .../weather_api/date=2025-10-11/

---
## Validaciones

se verifica creación de archivo (en AWS S3) y sincronización exitosa (Airbyte)

![aws](/pi_mod_04/assets/s3_evidence.png)

![airbyte](/pi_mod_04/assets/airbyte_evidence.png)

---

Mejoras Pendientes
  *  Automatizar validaciones.
  *  Implementar alertas o checks de consistencia.


--- 
### Conclusión 

La integración realizada en esta segunda entrega permitió dar el primer paso hacia la implementación del pipeline ETLT propuesto, abordando la fase de ingesta inicial de datos crudos (capa raw) en un Data Lake sobre Amazon S3.

A través de Airbyte, se logró configurar y validar exitosamente una conexión con una API pública (OpenWeatherMap), extrayendo datos meteorológicos en formato JSON, transformándolos automáticamente a formato Parquet con compresión Snappy, y almacenándolos de forma particionada en S3. Este proceso se alineó directamente con el diseño arquitectónico definido previamente, donde se propuso:

**Usar Airbyte como herramienta de ingesta flexible.**

**Preservar los datos en estado crudo para trazabilidad.**

**Utilizar formatos columnares eficientes para almacenamiento y posterior análisis.**


Más allá de lo técnico, esta entrega me permitió conectar mejor la teoría con la práctica, entender en profundidad cómo se instrumenta una arquitectura moderna de datos.