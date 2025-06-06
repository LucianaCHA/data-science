# import os
# import pandas as pd
# import mysql.connector

# DB_CONFIG = {
#     "host": "database",
#     "user": os.environ["MYSQL_USER"],
#     "password": os.environ["MYSQL_PASSWORD"],
#     "database": os.environ["MYSQL_DATABASE"],
# }

# TABLE_FILES = {
#     "categories": "categories.csv",
#     "countries": "countries.csv",
#     "cities": "cities.csv",
#     "customers": "customers.csv",
#     "employees": "employees.csv",
#     "products": "products.csv",
#     "sales": "sales.csv",
# }

# DATA_PATH = "/app/data"


# def insert_table_data(cursor, table, data_frame):
#     data_frame = data_frame.where(pd.notnull(data_frame), None)
#     columns = data_frame.columns.tolist()
#     placeholders = ", ".join(["%s"] * len(data_frame.columns))
#     columns_str = ", ".join(columns)
#     sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

#     for row in data_frame.itertuples(index=False, name=None):
#         cursor.execute(sql, row)


# def main():
#     print("conecting to db...")
#     conn = mysql.connector.connect(**DB_CONFIG)
#     cursor = conn.cursor()

#     for table, filename in TABLE_FILES.items():
#         filepath = f"{DATA_PATH}/{filename}"
#         print(f"inseert data into table: {table} from file: {filename}...")
#         df = pd.read_csv(filepath)
#         insert_table_data(cursor, table, df)
#         conn.commit()

#     cursor.close()
#     conn.close()
#     print("Load success.")


# if __name__ == "__main__":
#     main()


import os
import pandas as pd
import mysql.connector
from tqdm import tqdm
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

    cols = ', '.join(df.columns)
    placeholders = ', '.join(['%s'] * len(df.columns))
    sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

    data = df.to_records(index=False).tolist()

    total_batches = len(data) // batch_size + (1 if len(data) % batch_size else 0)
    inserted_rows = 0

    try:
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(sql, batch)
            conn.commit()
            inserted_rows += len(batch)
            print(f"  [Batch {i // batch_size + 1}/{total_batches}] Cargadas {inserted_rows} filas...")

    except Exception as e:
        print(f"Error al insertar en {table_name}: {e}")
        conn.rollback()

    # Comparar con la cantidad real en la base
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        db_rows = cursor.fetchone()[0]
    except Exception as e:
        db_rows = 'Error al contar'
        print(f"No se pudieron contar filas en '{table_name}': {e}")

    elapsed = time.time() - start_time
    print(f"[OK] '{table_name}' → CSV: {len(df)} | DB: {db_rows} filas")
    print(f"Tiempo: {elapsed:.2f} segundos\n")
# def insert_table_data(cursor, conn, table_name, df, batch_size=1000):
#     print(
#         f"[→] Insertando en '{table_name}' usando ejecutemany por bloques de {batch_size}..."
#     )
#     columns = ", ".join(df.columns)
#     placeholders = ", ".join(["%s"] * len(df.columns))
#     sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

#     data = [
#         tuple(None if pd.isna(val) else val for val in row) for row in df.to_numpy()
#     ]

#     total = len(data)
#     with tqdm(total=total, desc=f"{table_name}", unit="fila") as pbar:
#         for i in range(0, total, batch_size):
#             batch = data[i : i + batch_size]
#             try:
#                 cursor.executemany(sql, batch)
#                 conn.commit()
#             except mysql.connector.Error as err:
#                 print(f"[ERROR] Batch desde fila {i} hasta {i+batch_size}: {err}")
#             pbar.update(len(batch))


# def insert_table_data(cursor, table_name, df):
#     df = df.where(pd.notnull(df), None)
#     columns = df.columns.tolist()
#     if not columns:
#         print(f"[WARN] El archivo {table_name}.csv no tiene columnas válidas.")
#         return

#     placeholders = ", ".join(["%s"] * len(columns))
#     column_names = ", ".join(columns)
#     sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

#     total = len(df)
#     print(f"[INFO] Insertando {total} filas en '{table_name}'...")

#     for start in range(0, total, BATCH_SIZE):
#         end = min(start + BATCH_SIZE, total)
#         batch = df.iloc[start:end].itertuples(index=False, name=None)
#         try:
#             cursor.executemany(sql, list(batch))
#         except Exception as e:
#             print(f"[ERROR] Batch {start}-{end} en '{table_name}': {e}")
#             continue


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
                    print(f"[INFO] CSV '{filename}': {len(df)} filas detectadas")

                    insert_table_data(cursor, conn, table_name, df, BATCH_SIZE)
                    conn.commit()

                    db_count = get_table_row_count(cursor, table_name)
                    print(
                        f"[OK] '{table_name}' → CSV: {len(df)} | DB: {db_count} filas"
                    )
                except Exception as e:
                    print(f"[ERROR] Falló la carga para '{table_name}': {e}")
            else:
                print(f"[SKIP] No existe la tabla '{table_name}', archivo omitido.")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
