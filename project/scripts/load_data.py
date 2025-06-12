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
BATCH_SIZE = 100000
CHUNK_SIZE = 1000000


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

    df = df.where(pd.notnull(df), None)
    cols = ", ".join(df.columns)
    placeholders = ", ".join(["%s"] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = df.to_records(index=False).tolist()
    total_batches = len(data) // batch_size + (1 if len(data) % batch_size else 0)
    inserted_rows = 0

    try:
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            cursor.executemany(sql, batch)
            conn.commit()
            inserted_rows += len(batch)
            print(
                f"[Batch {i // batch_size + 1}/{total_batches}] Inserted {inserted_rows} rows..."
            )
    except Exception as e:
        print(f"Error al insertar en {table_name}: {e}")
        conn.rollback()


# check if db is empty if it is, insert data from csv files else skip
def is_table_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    return count == 0


def check_table_is_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    if count == 0:
        print(f"[INFO] La tabla '{table_name}' está vacía.")
        return True
    else:
        print(f"[INFO] La tabla '{table_name}' ya tiene datos. Omitiendo carga.")
        return False


def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    tables = get_existing_tables(cursor)
    print(f"[INFO] Tablas en la base: {tables}")

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".csv"):
            table_name = filename[:-4]

            if table_name in tables and is_table_empty(cursor, table_name):
                file_path = os.path.join(DATA_DIR, filename)

                try:
                    chunk_iter = pd.read_csv(file_path, chunksize=CHUNK_SIZE)
                    total_inserted = 0
                    chunk_count = 0
                    start_time = time.time()

                    for chunk in chunk_iter:
                        chunk_count += 1
                        print(
                            f"[INFO] Insertando chunk {chunk_count} ({len(chunk)} filas)..."
                        )
                        insert_table_data(cursor, conn, table_name, chunk, BATCH_SIZE)
                        total_inserted += len(chunk)

                    db_count = get_table_row_count(cursor, table_name)
                    elapsed = time.time() - start_time

                    print(
                        f"[OK] '{table_name}' → CSV: {total_inserted} | DB: {db_count} filas"
                    )
                    print(f"Tiempo total: {elapsed:.2f} segundos\n")

                except Exception as e:
                    print(f"[ERROR] Falló la carga para '{table_name}': {e}")
            else:
                print(
                    f"[SKIP] La tabla '{table_name}' no existe o ya tiene datos. Archivo omitido."
                )

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
