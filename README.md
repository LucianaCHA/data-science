# Proyecto Integrador - Curso Data Engineering

## Resumen

Las entregas solicitadas se presentan en el directorio [`delivery`](./project/delivery/) :

* Entrega 1 - 

   1 .[`Documento técnico `](/pi_mod_03/delivery/01-first-delivery/tech-document.md): Se brinda documento técnico requerido incluyendo diagrama de arquitectura, stack tecnológico.

   2.[`Roadmap `](/pi_mod_03/delivery/01-first-delivery/roadmap.md): Propuesta de pasos de desarrollo de la propuesta técnica

* Entrega 2 - 
   1. [`Documento técnico`](/pi_mod_03/delivery/02-second-delivery/2nd_delivery.md): Informe de pipeline implementado para capa raw con acceso a imagen desplegada e instrucciones para su uso en google cloud.

* Entrega 3 - 
   1.  [`Documento técnico`](/pi_mod_03/delivery/03-third-delivery/3rd_delivery.md): Informe de pipeline implementado para capa raw con acceso a imagen desplegada e instrucciones para su uso en google cloud.

## Detalles del Proyecto

Este proyecto fue desarrollado dentro de un **entorno Dockerizado**, para facilitar configuración y ejecución del sistema en diferentes entornos. Los siguientes servicios fueron dockerizados:

1. **Base de Datos (Postgress)**: 
   Se utilizó la imagen oficial de **Postgress** para crear un contenedor que aloja la base de datos del proyecto. La configuración de la base de datos, incluida la creación de tablas y la carga de datos desde los archivos sql proporcionados, se realiza mediante un archivo SQL que se inicializa automáticamente al levantar el contenedor.

2. **ADminer** Se utilizó Adminer como una herramienta web para la administración de bases de datos. Este contenedor facilita la interacción con la base de datos MySQL a través de una interfaz gráfica. Expuesto en puerto 8080

3. **Pi_mod_03**:
El proyecto en sí mismo también está dockerizado. Se utilizó un contenedor basado en Python 3.11 que ejecuta el código preparado para su ejecuión en google cloud o en entorno local.

## Requerimientos para levantar el proyecto localmente

- Python >= 3.11
- Docker <= 28.1.1

## Estructura del proyecto

`pi_mod_02/`
 - `app/`
   - `assets/` -  Archivos de recursos (CSV, imágenes, etc.)
   - `config/` - Configuración general del proyecto
   - `db/`     - Módulo de conexión y operaciones con la base de datos
   - `loader/` - Clases para la carga de datos
   - `models/' - Modelos de datos (clases, validaciones)
   - `repository/` - Capa de abstracción de operaciones con datos
   - `utils/`       -Funciones auxiliares y utilitarias

 - `dbt_project/` - Proyecto DBT para transformación de datos
 - `delivery/` - Directorio que contiene los requerimientos de cada avance
   - 01-delivery (primer entrega)
   - 02-delivery (segunda entrega)
   - 03-delivery (tercer entrega)
 - `scripts/` - Scripts de inicialización y gestión del proyecto
   - `db/` 
      - `data/` - incluye los sql para popular tablas
         - [`01_init__db.sql/`](/pi_mod_02/scripts/db/01_init_db.sql) - Script para vrea base de datos.
         - [`init.sh/`](./project/scripts/init.sh) - Inicializa proyecto, docker , instalación de dependencias , base de datos, etc.
 - `requirements.txt/` 


## Instalación

Renombrar el archivo `.env.example` a `.env` y definir las variables de entorno necesarias [Variables de entorno](#variables-de-entorno)


## Inicialización de base de datos 

El proyecto ejecuta un script para crear base de datos y tablas requeridas por el proyecto. Para popularlas , se utiliza SQLAlchemy para la creación de las tablas y la carga inicial de datos.

Los datos se cargan a partir de archivos sql alojados en el directorio scripts/db/data/.

Cada conjunto de datos tiene un loader dedicado, basado en la clase abstracta DataLoader, que gestiona su lectura, parseo e inserción.

### Setup ambiente de desarrollo con docker compose

Para construir imágenes:
```bash
docker compose -p project build
```

para correr el proyecto
```bash
docker compose -p project up
```

Para detener contenedores (Ctrl + c)
```bash
docker compose -p project stop
```

Para eliminar imágenes [con la opción -v, se borran todas las actualizaciones del dump inicial, y cuando se levante nuevamente, lo hará con los datos iniciales de /data]
```bash
docker compose -p project down [-v]
```

## Adminer:

Se disponibiliza un adminer en 

http://localhost:8080/?pgsql=database&username=${POSTGRES_USER}&db=ecommerce_db

Segun lo definido para la env ${POSTGRES_USER} 

## Cómo conectarse a docker

Si por alguna razón se necesita conectarse al docker de este proyecto

``docker exec -it <:docker_name> bash``

## Variables de entorno

Están ubicadas en el archivo `.env.example`

### `POSTGRES_*`
- Utilizadas para la BD de `docker compose`

**Nota** Se debe mantener el nombre de la base de datos como __airbnb-db__ y las envs de los path tal cual se brindan en el archivo env_example


# Instrucciones despliegue en GCloud