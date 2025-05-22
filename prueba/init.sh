#!/bin/bash

pip install --no-cache-dir python-decouple python-dotenv numpy notebook pandas

echo "holas ! Iniciando Jupyter Notebook..."

jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
