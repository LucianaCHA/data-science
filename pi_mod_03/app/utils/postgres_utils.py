import pandas as pd
from app.db.session import engine


def run_query(query: str, params=None):
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn, params=params)


def run_non_select_query(query: str, params=None):
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(query, params)
