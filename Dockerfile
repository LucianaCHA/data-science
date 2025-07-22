FROM python:3.11-slim

LABEL maintainer="lucianachamorro87@gmail.com"

WORKDIR /app
ENV PYTHONPATH="/app" 
COPY pi_mod_02/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY pi_mod_02/scripts/init.sh /init.sh
RUN chmod +x /init.sh

ENTRYPOINT ["bash", "/init.sh"]
