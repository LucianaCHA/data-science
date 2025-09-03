#!/bin/bash
set -e

echo "Esperando conexión a la base de datos..."

python3 - <<EOF
import time
import psycopg2
from psycopg2 import OperationalError
import os

db_host = os.getenv("DB_HOST", "database")
db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")

print(f"Intentando conectar a {db_host}...")

while True:
    try:
        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            dbname="postgres"
        )
        conn.close()
        print("Conexión a PostgreSQL establecida.")
        break
    except OperationalError as e:
        print(f"PostgreSQL aún no disponible... {e}")
        time.sleep(2)
EOF

echo "Verificando base de datos '$POSTGRES_DB'..."
PGPASSWORD=$POSTGRES_PASSWORD psql \
  -h $DB_HOST -U $POSTGRES_USER -d postgres \
  -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || \
PGPASSWORD=$POSTGRES_PASSWORD psql \
  -h $DB_HOST -U $POSTGRES_USER -d postgres \
  -c "CREATE DATABASE \"$POSTGRES_DB\";"

echo "Base de datos '$POSTGRES_DB' lista."

# Ejecutar todos los scripts .sql en /app/scripts/db
SQL_DIR="/app/scripts/db"
if [ -d "$SQL_DIR" ]; then
    for script in "$SQL_DIR"/*.sql; do
        if [ -f "$script" ]; then
            echo "Ejecutando $script..."
            PGPASSWORD=$POSTGRES_PASSWORD psql \
              -h $DB_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f "$script"
        fi
    done
else
    echo "No hay carpeta $SQL_DIR, no se aplicaron scripts SQL."
fi

python3 /app/app/raw/scripts/loader.py

exec uvicorn app.main:app --host 0.0.0.0 --port 8888
echo "Inicialización completa."
