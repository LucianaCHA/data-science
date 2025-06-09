import os
import pandas as pd
import mysql.connector

import time

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "database"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "sales_company"),
}

DATA_DIR = "/app/data"
BATCH_SIZE = 10000


def connect_to_db():
    return mysql.connector.connect(**DB_CONFIG)


def get_existing_tables(cursor):
    cursor.execute("SHOW TABLES")
    return set(row[0] for row in cursor.fetchall())


def get_table_row_count(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0]


def insert_table_data(cursor, conn, table_name, df, batch_size=1000):
    print(f"[INFO] Insertando datos en '{table_name}' desde CSV...")

    start_time = time.time()
    df = df.where(pd.notnull(df), None)

    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = df.to_records(index=False).tolist()

    total_batches = len(data) // batch_size + (
        1 if len(data) % batch_size else 0)
    inserted_rows = 0

    try:
        for i in range(0, len(data), batch_size):
            batch = data[i: i + batch_size]
            cursor.executemany(sql, batch)
            conn.commit()
            inserted_rows += len(batch)
            print(
                f"""[Batch {i // batch_size + 1}/{total_batches}]
                Alrready inserted {inserted_rows} rows..."""
            )

    except Exception as e:
        print(f"Error al insertar en {table_name}: {e}")
        conn.rollback()

    # Comparar con la cantidad real en la base
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        db_rows = cursor.fetchone()[0]
    except Exception as e:
        db_rows = "Failed to count"
        print(f"No se pudieron contar filas en '{table_name}': {e}")

    elapsed = time.time() - start_time
    print(f"[OK] '{table_name}' → CSV: {len(df)} | DB: {db_rows} filas")
    print(f"Time: {elapsed:.2f} secs\n")


def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    tables = get_existing_tables(cursor)
    print(f"[INFO] Tablas en la base: {tables}")

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            table_name = filename[:-4]

            if table_name in tables:
                try:
                    file_path = os.path.join(DATA_DIR, filename)
                    df = pd.read_csv(file_path)
                    print(
                        f"""[INFO] CSV '{filename}':
                        {len(df)} detected rows """
                    )

                    insert_table_data(cursor, conn, table_name, df, BATCH_SIZE)
                    conn.commit()

                    db_count = get_table_row_count(cursor, table_name)
                    print(
                        f"""[OK] '{table_name}' → CSV: {len(df)}
                        | DB: {db_count} rows"""
                    )
                except Exception as e:
                    print(f"[ERROR] Falló la carga para '{table_name}': {e}")
            else:
                print(
                    f"""[SKIP] Table does not exists '{table_name}'
                      , omitted file."""
                )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
