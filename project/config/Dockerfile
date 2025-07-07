FROM python:3.11-slim

LABEL maintainer="lucianachamorro87@gmail.com"

WORKDIR /app

COPY project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY project/scripts/init.sh /init.sh
RUN chmod +x /init.sh

ENTRYPOINT ["bash", "/init.sh"]
