import os
from load_data import connect_to_db
import mysql.connector


def create_trigger(cursor):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sql_path = os.path.join(current_dir, "create_trigger.sql")

        with open(sql_path, "r") as file:
            trigger_sql = file.read()

        cursor.execute(trigger_sql)
        print("[OK] Trigger creado exitosamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo crear el trigger: {e}")


def main():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        create_trigger(cursor)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"[ERROR] Error de conexión a la base de datos: {err}")
    finally:
        if cursor:
            cursor.close()
        print("[INFO] Script de creación de trigger completado.")


main()
