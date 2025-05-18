from decouple import config

# Leer las variables de entorno desde el archivo .env
db_host = config('DB_HOST')
db_port = config('DB_PORT', cast=int)  # Convertir a entero
db_user = config('DB_USER')
db_password = config('DB_PASSWORD')

db_name = config('DB_NAME')

print(f"Host: {db_host}")
print(f"Port: {db_port}")
print(f"User: {db_user}")
print(f"Password: {db_password}")
print(f"Database: {db_name}")