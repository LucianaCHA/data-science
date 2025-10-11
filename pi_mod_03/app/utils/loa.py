from google.cloud import storage
import pandas as pd
import io

def download_csv_from_gcs(bucket_name, file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    data = blob.download_as_bytes()
    df = pd.read_csv(io.BytesIO(data))
    return df
from sqlalchemy import create_engine
import pandas as pd

def get_engine(db_config):
    user = db_config["user"]
    password = db_config["password"]
    host = db_config["host"]
    dbname = db_config["dbname"]
    port = db_config["port"]

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
    return create_engine(url)

def load_dataframe_to_postgres(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists='replace', index=False)
import yaml
from utils.gcs import download_csv_from_gcs
from utils.db import get_engine, load_dataframe_to_postgres

def main():
    # Cargar config
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    # Descargar CSV desde GCS
    df = download_csv_from_gcs(config["gcs"]["bucket"], config["gcs"]["file_path"])

    # Crear engine y cargar en Postgres
    engine = get_engine(config["postgres"])
    load_dataframe_to_postgres(df, config["postgres"]["table_name"], engine)

if __name__ == "__main__":
    main()
gcs:
  bucket: my-data-bucket
  file_path: data/raw/my_file.csv

postgres:
  host: /cloudsql/my-cloudsql-instance-id  # Para conexión desde GCP
  port: 5432
  user: myuser
  password: mypass
  dbname: raw_db
  table_name: raw_my_data
import pandas as pd
import json
from datetime import datetime
from utils.db import get_engine
import yaml

EXPECTED_COLUMNS = {
    "id": "int64",
    "name": "object",
    "created_at": "datetime64[ns]",
    "amount": "float64"
}

UNIQUE_KEY = ["id"]

def validate_data(df):
    report = {}
    report['timestamp'] = datetime.utcnow().isoformat()
    report['null_values'] = df.isnull().sum().to_dict()

    report['dtypes'] = df.dtypes.astype(str).to_dict()
    report['expected_types'] = {col: str(dtype) for col, dtype in EXPECTED_COLUMNS.items()}

    report['columns_present'] = list(df.columns)
    report['missing_columns'] = list(set(EXPECTED_COLUMNS.keys()) - set(df.columns))

    if UNIQUE_KEY:
        report['duplicate_keys'] = df.duplicated(subset=UNIQUE_KEY).sum()

    # Coherencia
    if 'amount' in df.columns:
        report['negative_amounts'] = (df['amount'] < 0).sum()

    if 'created_at' in df.columns:
        invalid_dates = pd.to_datetime(df['created_at'], errors='coerce').isnull().sum()
        report['invalid_dates'] = invalid_dates

    return report

def main():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    engine = get_engine(config["postgres"])
    df = pd.read_sql(f"SELECT * FROM {config['postgres']['table_name']}", engine)

    report = validate_data(df)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    with open(f"reports/validation_report_{timestamp}.json", "w") as f:
        json.dump(report, f, indent=4)

    print(f"✅ Reporte generado: validation_report_{timestamp}.json")

if __name__ == "__main__":
    main()
