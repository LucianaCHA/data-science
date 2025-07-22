# Proyecto Integrador - Curso Data Engineering

## Resumen

Las consignas solicitadas se presentan en formato markdown en el directorio [`delivery`](./project/delivery/) :

1.[`Avance 1`](./project/delivery/01-first-delivery/project_answers_screenshots.md)

2.[`Avance 2`](./project/delivery/02-second-delivery/project_answers_screenshots.md)

3.[`Avance 3`](./project/delivery/03-third-delivery/)

Y en formato Notebook en:

1.[`Avance 1`](./project/1st_delivery.ipynb)

2.[`Avance 2`](./project/2nd_delivery.ipynb)

3.[`Avance 3`](./project/3rd_delivery.ipynb)


Finalmente, se añadió el notebook [`project_overview`](./project/project_overview.ipynb), que sirve como presentación del proyecto. En este documento también se ofrece la opción de ejecutar consultas que permiten verificar que los datos proporcionados en los archivos CSV fueron correctamente cargados en la base de datos, lo cual es esencial para la resolución de las consignas planteadas.

## Detalles del Proyecto

Este proyecto fue desarrollado dentro de un **entorno Dockerizado**, para facilitar configuración y ejecución del sistema en diferentes entornos. Los siguientes servicios fueron dockerizados:

1. **Base de Datos (MySQL)**: 
   Se utilizó la imagen oficial de **MySQL 8.0** para crear un contenedor que aloja la base de datos del proyecto. La configuración de la base de datos, incluida la creación de tablas y la carga de datos desde los archivos CSV proporcionados, se realiza mediante un archivo SQL que se inicializa automáticamente al levantar el contenedor.

2. **ADminer** Se utilizó Adminer como una herramienta web para la administración de bases de datos. Este contenedor facilita la interacción con la base de datos MySQL a través de una interfaz gráfica. Expuesto en puerto 8080

3. **Proyecto Integrador**:
El proyecto en sí mismo también está dockerizado. Se utilizó un contenedor basado en Python 3.11 que ejecuta el código y los notebooks del proyecto. Estos están disponibles en el puerto 8888 para realizar consultas interactivas y revisar  resultados.

## Requerimientos para levantar el proyecto localmente

- Python >= 3.11
- Docker <= 28.1.1

## Estructura del proyecto

`project/`
- `assets/` - Directorio de imágenes
   - 00-images
   - 01-images
   - **-images (donde ** refiere al nro de entrega)
 - `data/` - Aquí deben incluirse los archivos CSV para popular la tablas
 - `delivery/` - Directorio que contiene las respuestas de cada avance
   - 01-delivery (primer entrega)
      - [`md_answers_file/`](./project/delivery/01-first-delivery/project_answers_screenshots.md)
   - 02-delivery (segunda entrega)
      - [`md_answers_file/`](./project/delivery/02-second-delivery/project_answers_screenshots.md)
   - **-delivery (donde ** refere al nro de entrega)
 - `scripts/` - Scripts de inicialización y gestión del proyecto
   - [`01_init_db.sql/`](./project/scripts/01_init_db.sql) - Inicialización base de datos sales_company
   - [`02_init_monitoring_table.sql/`](./project/scripts/02_init_monitoring_table.sql) - Adición tabla de monitoreo de ventas
   - [`create_trigger.sql/`](./project/scripts/create_trigger.sql) - Query creaciòn de trigger umbral 200 mil ventas
   - [`create_trigger.py/`](./project/scripts/create_trigger.sql) - Script que ejecuta query sql anterior.
   - [`init.sh/`](./project/scripts/init.sh) - Inicializa proyecto, docker , instalación de dependencias , base de datos, etc.
   - [`load_data.py/`](./project/scripts/load_data.py) - Script para carga de datos de csv a la base de datos
 - `utils/` - Utilidades/módulos varios reutilzables en el proyecto
 - `project_overview.ipynb/` - Introducción y reporte de datos
 - `requirements.txt/` 


## Instalación

Renombrar el archivo `.env.example` a `.env` y definir las variables de entorno necesarias [Variables de entorno](#variables-de-entorno)


## Inicialización de base de datos 

El proyecto ejecuta un script para crear base de datos y tablas requeridas por el proyecto. Para popularlas , se deben agregar los archivos CSV necesarios en el directorio data.

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

###  Acceso a Jupyter Notebook

Una vez que el contenedor esté corriendo, se puede acceder a Jupyter Notebook desde el navegador:

- **Puerto por defecto (8888)**: http://localhost:8888

Ingresar el password o token '1234'

## Adminer:

Se disponibiliza un adminer en 

http://localhost:8080/?pgsql=database&username=${MYSQL_USER}&db=ecommerce_db

Segun lo definido para la env ${MYSQL_USER} 

## Cómo conectarse a docker

Si por alguna razón se necesita conectarse al docker de este proyecto

``docker exec -it <:docker_name> bash``

## Variables de entorno

Están ubicadas en el archivo `.env.example`

### `MYSQL_*`
- Utilizadas para la BD de `docker compose`

**Nota** Se debe mantener el nombre de la base de datos como __sales_company__ y las envs de los path tal cual se brindan en el archivo env_example
