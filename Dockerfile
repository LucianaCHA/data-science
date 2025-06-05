FROM python:3.11-slim

# Instala bash y utilidades necesarias
RUN apt-get update && apt-get install -y bash && apt-get clean

# Establece directorio de trabajo
WORKDIR /app

# Copia el script y da permisos de ejecución
COPY scripts/init.sh /init.sh
RUN chmod +x /init.sh

# Usa bash explícitamente para ejecutar el script
ENTRYPOINT ["bash", "/init.sh"]
