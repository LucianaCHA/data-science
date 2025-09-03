#!/bin/bash
set -e

# Crear la base de datos si no existe
psql -U "$POSTGRES_USER" -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'airbnb-db'" | grep -q 1 || \
psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE airbnb-db;"

echo "db 'airbnb-db' lista."

# Ejecutar los scripts de inicialización (asegurate que existan en la carpeta montada)
if [ -f /docker-entrypoint-initdb.d/01_init_db.sql ]; then
    echo " ejecuta 01_init_db.sql..."
    psql -U "$POSTGRES_USER" -d airbnb-db -f /docker-entrypoint-initdb.d/01_init_db.sql
fi

if [ -f /docker-entrypoint-initdb.d/init_create_audit_table.sql ]; then
    echo "ejecuta init_create_audit_table.sql..."
    psql -U "$POSTGRES_USER" -d airbnb-db -f /docker-entrypoint-initdb.d/init_create_audit_table.sql
fi

echo "inicializacion completada."
