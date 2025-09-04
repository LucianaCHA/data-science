#!/bin/bash
set -e

echo "Esperando conexión a la base de datos..."

python3 /app/app/raw/scripts/loader.py

echo "==> Ejecutando validacion de datos..."
python3 /app/app/stage/scripts/loader.py


exec uvicorn app.main:app --host 0.0.0.0 --port 8888 

echo "Inicialización completa."
