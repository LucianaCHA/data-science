LABEL maintainer="lucianachamorro87@gmail.com"

FROM apache/spark:3.5.7-scala2.12-java17-python3-r-ubuntu

USER root

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
COPY app/ /app/