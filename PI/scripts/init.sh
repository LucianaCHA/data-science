#!/bin/bash

echo "is db ready? ..."
python3 - <<EOF
import time
import mysql.connector
from mysql.connector import Error

while True:
    try:
        conn = mysql.connector.connect(
            host='database',
            user='${MYSQL_USER}',
            password='${MYSQL_PASSWORD}',
            database='${MYSQL_DATABASE}'
        )
        if conn.is_connected():
            print("Conexión establecida.")
            conn.close()
            break
    except Error as e:
        print("Esperando conexión a MySQL...")
        time.sleep(2)
EOF

echo "populando base con csv..."
python3 /app/scripts/load_data.py

echo "holas ! Iniciando Jupyter Notebook..."

jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token='1234' --NotebookApp.password='1234'
