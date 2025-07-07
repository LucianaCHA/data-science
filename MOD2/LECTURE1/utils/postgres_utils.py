import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import warnings

load_dotenv()
warnings.filterwarnings("ignore", category=UserWarning)


def connect_to_db():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "database"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        dbname=os.getenv("POSTGRES_DATABASE", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

def run_query(query: str, params=None):
    conn = connect_to_db()
    try:
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()

def run_non_select_query(query: str, params=None):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
    except Exception as e:
        print("Error:", e)
        conn.rollback()
    finally:
        conn.close()