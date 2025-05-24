FROM python:3.11-slim

WORKDIR /app

COPY scripts/init.sh /init.sh
RUN chmod +x /init.sh


# docker-compose down -v --remove-orphans
# -v: borra los volúmenes asociados
# --remove-orphans: elimina contenedores creados por compose que ya no están definidos 

