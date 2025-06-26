#!/bin/bash

echo "¿Está lista la base de datos? ..."
python3 - <<EOF
import time
import psycopg2
from psycopg2 import OperationalError
import os

while True:
    try:
        conn = psycopg2.connect(
            host='database',
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            # dbname=os.environ['POSTGRES_DATABASE']
        )
        print("Conexión establecida.")
        conn.close()
        break
    except OperationalError:
        print("Esperando conexión a PostgreSQL...")
        time.sleep(2)
EOF

# echo "Populando base con CSV..."
# python3 /app/scripts/load_data.py

# echo "Creando trigger para monitoreo de ventas..."
# python3 /app/scripts/create_trigger.py

echo "¡Holas! Iniciando Jupyter Notebook..."
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser \
    --NotebookApp.token='1234' --NotebookApp.password='1234'
