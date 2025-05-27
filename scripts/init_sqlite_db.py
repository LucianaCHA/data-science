import sqlite3

# Ajusta el path a la base, por ejemplo: "MO1/L3/sales.db"
db_path = "sales.db"  # Cambia por el path correcto si hace falta

# Conexión a la base SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

print("Tablas disponibles:")
for tabla in tablas:
    print(f"- {tabla[0]}")

# Mostrar primeras 3 filas de cada tabla
for tabla in tablas:
    print(f"\nPrimeras 3 filas de la tabla '{tabla[0]}':")
    cursor.execute(f"SELECT * FROM {tabla[0]} LIMIT 3")
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)

conn.close()
