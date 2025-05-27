#!/bin/bash

pip install --no-cache-dir python-decouple python-dotenv numpy notebook pandas

echo "Validando base de datos..."
python3 /init_db.py

echo "holas ! Iniciando Jupyter Notebook..."

jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser

