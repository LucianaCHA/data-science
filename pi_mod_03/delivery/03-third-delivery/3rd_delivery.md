# Análisis de Datos de Airbnb

Este proyecto realiza un **análisis exploratorio de datos de Airbnb**.  
A partir de una tabla cruda (`airbnb_raw`), se genera una tabla de dimensión (`rooms_dim`) con datos preparados para análisis.  
Posteriormente, se ejecutan **consultas SQL** para responder preguntas de negocio clave y se genera un **reporte HTML** con los resultados.

---

## ¿Qué hace el pipeline?

- Crea la tabla `rooms_dim` en **PostgreSQL** si no existe.
- Inserta datos directamente desde `airbnb_raw`, sin depender de otras tablas (por ejemplo, `room_types`).
- Ejecuta múltiples consultas SQL sobre `rooms_dim`, entre ellas:
  - Precio promedio por barrio y distrito.
  - Tipo de habitación más ofrecido y con mayor revenue estimado.
  - Análisis de anfitriones con más propiedades.
  - Comparativa de disponibilidad anual por barrio y tipo de habitación.
  - Evolución mensual de reseñas.
  - Detección de outliers en precios.
  - Relación entre disponibilidad anual y cantidad de reseñas (proxy de ocupación).
- Genera un **reporte HTML** con `pandas` y `jinja2`.
- Sube el reporte a un **bucket de Google Cloud Storage**.

---

##  Resultado en HTML

Puedes visualizar el reporte en el siguiente enlace:

[**Ver reporte HTML generado**](https://pi-mod03-data-ingestion-stage-314936653450.europe-west1.run.app/)

---

## Imagen Docker

El proyecto está contenido en una **imagen Docker** que puede ejecutarse localmente o desplegarse en la nube:

```bash
docker pull lucianacha/pi-mod03-data-ingestion/general