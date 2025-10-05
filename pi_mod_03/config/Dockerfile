# Imagen base ligera de Python 3.11
FROM python:3.11-slim

LABEL maintainer="lucianachamorro87@gmail.com"

# Establecer directorio de trabajo
WORKDIR /app
ENV PYTHONPATH="/app"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    bash \
    gcc \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python
COPY pi_mod_03/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts y código fuente
COPY pi_mod_03 /app
COPY pi_mod_03/scripts/main.sh /main.sh

# Dar permisos de ejecución
RUN chmod +x /main.sh

# Definir comando de inicio
ENTRYPOINT ["bash", "/main.sh"]
