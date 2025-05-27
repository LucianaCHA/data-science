FROM python:3.11-slim

WORKDIR /app

COPY scripts/init_sqlite_db.py /init_db.py
COPY scripts/init.sh /init.sh

RUN chmod +x /init.sh

CMD ["/init.sh"]
