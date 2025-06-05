import os
from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()


def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "database"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "pass"),
        database=os.getenv("MYSQL_DATABASE", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


def close_connection(conn):
    if conn.is_connected():
        conn.close()


def run_query(query: str, params=None):
    connection = connect_to_db()
    try:
        return pd.read_sql(query, connection, params=params)
    finally:
        close_connection(connection)


def run_non_select_query(query: str):
    connection = connect_to_db()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()
    finally:
        cursor.close()
        print("cerrando conexión, sin errores en la consulta")
        connection.close()
