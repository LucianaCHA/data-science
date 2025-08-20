#!/bin/bash

echo "¿Está lista la base de datos? ..."
python3 - <<EOF
import time
import psycopg2
from psycopg2 import OperationalError
import os

# Verificar repetidamente si la base de datos está disponible.
while True:
    try:
        conn = psycopg2.connect(
            host='database',
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            dbname=os.environ['POSTGRES_DB']
        )
        print("Conexión establecida!!!!!!!!!!!!!!11.")
        
        # Intentar crear la base de datos si no existe
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;") 
        conn.close()
        break
    except OperationalError:
        print("Esperando conexión a PostgreSQL...")
        time.sleep(2)
EOF

echo "Ejecutando script de inicialización de base de datos..."

python3 /app/app/loader/load_all.py


# --- NUEVO BLOQUE: Exportar la app Marimo a HTML-WASM ---
echo "🛠️ Exportando notebook Marimo a HTML interactivo..."
marimo export html-wasm marimo/notebooks/notebook.py -o /app/docs --mode run

# Agregar .nojekyll automáticamente
touch /app/docs/.nojekyll

echo "✅ Exportación completa. Archivos listos en /app/docs"

# --- OPCIONAL: arrancar Marimo como servidor (si querés usarlo en tiempo real) ---
# echo "📡 Iniciando Marimo en modo servidor..."
marimo run marimo/notebooks/notebook.py --host 0.0.0.0 --port 8888