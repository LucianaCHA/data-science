# Proyecto Integrador - Curso Data Engineering

## Resumen

Las consignas solicitadas se presentan en dos secciones principales:

1. **`[nro de entrega]_delivery_live_answers`**: En estos notebook se encuentran las consultas en vivo que resuelven las consignas planteadas. Aquí se ejecutan las consultas directamente y se presentan los resultados generados en tiempo real.
  
2. **`/delivery/[nro de entrega]project_answers_screenshots.md`**: Se presentan las solucions y respuestas propuestas en formato markdown.

Finalmente, se añadió el notebook **`project_overview`**, que sirve como presentación del proyecto. En este documento también se ofrece la opción de ejecutar consultas que permiten verificar que los datos proporcionados en los archivos CSV fueron correctamente cargados en la base de datos, lo cual es esencial para la resolución de las consignas planteadas.

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

`PI/`
- `assets/` - Directorio de imágenes
   - 00-images
   - 01-images
   - **-images (donde ** refere al nro de entrega)
 - `data/` - Aquí deben incluirse los archivos CSV para popular la tablas
 - `delivery/` - Directorio que contiene las respuestas de cada avance
   - 00-delivery (primer entrega)
      - [`md_answers_file/`](./app/PI/delivery/00-first-delivery/project_answers_screenshots.md)
   - 01-delivery (segunda entrega)
      - [`md_answers_file/`](./app/PI/delivery/01-second-delivery/project_answers_screenshots.md)
   - **-delivery (donde ** refere al nro de entrega)
 - `scripts/` - Scripts de inicialización y gestión del proyecto
 - `utils/` - Utilidades/módulos varios reutilzables en el proyecto
 - `*_live_answers.ipynb/` - En estos archivo se ejecutan las consultas y se muestran las respuestas directamente desde la base de datos. 
   - [`first_delivery/`](./app/PI/1st_delivery_live_answers.ipynb)
   - [`second_deliver/`](./app/PI/2nd_delivery_live_answers.ipynb)
 - `project_overview.ipynb/` - Introducción y reporte de datos
 - `project_answers_screenshots.ipynb/` - Consultas con resultados visualizados
 - `requirements.txt/` 


## Instalación

Renombrar el archivo `.env.example` a `.env` y definir las variables de entorno necesarias [Variables de entorno](#variables-de-entorno)


## Inicialización de base de datos 

El proyecto ejecuta un script para crear base de datos y tablas requeridas por el proyecto. Para popularlas , se deben agregar los archivos CSV necesarios en el directorio data

### Setup ambiente de desarrollo con docker compose

Para construir imágenes:
```bash
docker compose -p integrator_project build
```

para correr el proyecto
```bash
docker compose -p integrator_project up
```

Para detener contenedores (Ctrl + c)
```bash
docker compose -p integrator_project stop
```

Para eliminar imágenes [con la opción -v, se borran todas las actualizaciones del dump inicial, y cuando se levante nuevamente, lo hará con los datos iniciales de /data]
```bash
docker compose -p integrator_project down [-v]
```

###  Acceso a Jupyter Notebook

Una vez que el contenedor esté corriendo, se puede acceder a Jupyter Notebook desde el navegador:

- **Puerto por defecto (8888)**: `http://localhost:8888`

Ingresar el password o token '1234'

## Adminer:

Se disponibiliza un adminer en 

http://[::]:8080/?server=database&username=${MYSQL_USER}&db=sales_company
o (en Windows)
http://localhost:8080/?server=database&username=${MYSQL_USER}&db=sales_company

Segun lo definido para la env ${MYSQL_USER} 

## Cómo conectarse a docker

Si por alguna razón se necesita conectarse al docker de este proyecto

``docker exec -it <:docker_name> bash``

## Variables de entorno

Están ubicadas en el archivo `.env.example`

### `MYSQL_*`
- Utilizadas para la BD de `docker compose`

**Nota** Se debe mantener el nombre de la base de datos como __sales_company__ y las envs de los path tal cual se brindan en el archivo env_example
