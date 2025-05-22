# Usamos una imagen base oficial de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app
COPY init.sh /init.sh
RUN chmod +x /init.sh

COPY /app /app/

# CMD ["python", "script.py"]
