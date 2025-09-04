import pandas as pd
from google.cloud import storage
from app.config.config import Settings
from app.utils.date_utils import NOW
from app.services.htm_report import upload_html_report
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import io
from datetime import datetime
import json

from app.services.logger.gcloud_logger import CloudLogger


logger = CloudLogger()


EXPECTED_COLUMNS = [
    "id",
    "name",
    "host_id",
    "host_name",
    "neighbourhood_group",
    "neighbourhood",
    "latitude",
    "longitude",
    "room_type",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "last_review",
    "reviews_per_month",
    "calculated_host_listings_count",
    "availability_365",
]


def download_csv(bucket_name, file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    data = blob.download_as_bytes()
    return pd.read_csv(io.BytesIO(data))


def validate_dataframe(df: pd.DataFrame, file_name: str) -> dict:
    report = {"file": file_name, "timestamp": datetime.utcnow().isoformat()}

    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    report["missing_columns"] = missing_cols
    report["columns_ok"] = len(missing_cols) == 0

    # Calidad: nulos
    null_counts = df.isnull().sum().to_dict()
    report["nulls"] = null_counts

    # Calidad: tipos de datos
    type_issues = {}
    for col, expected_type in {
        "id": "int64",
        "latitude": "float64",
        "longitude": "float64",
        "price": "int64",
    }.items():
        if col in df.columns and df[col].dtype != expected_type:
            type_issues[col] = str(df[col].dtype)
    report["type_issues"] = type_issues

    # Calidad: unicidad de clave
    if "id" in df.columns:
        duplicates = df["id"].duplicated().sum()
        report["duplicate_ids"] = int(duplicates)
    else:
        report["duplicate_ids"] = "id column missing"

    # Coherencia: valores válidos
    if "latitude" in df.columns and "longitude" in df.columns:
        invalid_coords = df[
            ~df["latitude"].between(-90, 90) | ~df["longitude"].between(-180, 180)
        ]
        report["invalid_coords"] = len(invalid_coords)
    else:
        report["invalid_coords"] = "coords missing"

    if "price" in df.columns:
        invalid_price = len(df[df["price"] < 0])
        report["invalid_price"] = invalid_price

    return report


def upload_report(bucket_name, report, file_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    report_path = f"reports/{file_name.replace('/', '_')}_{NOW}.json"
    blob = bucket.blob(report_path)
    blob.upload_from_string(
        json.dumps(report, indent=2), content_type="application/json"
    )
    logger.info(
        "Reporr uploaded", extra={"gcs_path": f"gs://{bucket_name}/{report_path}"}
    )


def prepare_dataframe(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    if "last_review" in df.columns:
        df["last_review"] = pd.to_datetime(df["last_review"], errors="coerce")
    df["source_file"] = source_file
    df["ingested_at"] = NOW
    return df


def create_table(engine):
    create_sql = """
    CREATE TABLE IF NOT EXISTS airbnb_raw (
        id INTEGER PRIMARY KEY,
        name TEXT,
        host_id INTEGER,
        host_name TEXT,
        neighbourhood_group TEXT,
        neighbourhood TEXT,
        latitude FLOAT,
        longitude FLOAT,
        room_type TEXT,
        price INTEGER,
        minimum_nights INTEGER,
        number_of_reviews INTEGER,
        last_review DATE,
        reviews_per_month FLOAT,
        calculated_host_listings_count INTEGER,
        availability_365 INTEGER,
        source_file TEXT,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.connect() as conn:
        conn.execute(text(create_sql))


def load_to_postgres(df, engine):
    try:
        df.to_sql("airbnb_raw", engine, if_exists="append", index=False, method="multi")
    except IntegrityError as e:
        logger.error(f"Error inserting data (possible duplicate id): {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")


def main():
    config = Settings()
    bucket = config.GCS_BUCKET
    file_path = config.GCS_FILE_PATH
    db_url = config.DB_URL

    logger.info("Starting data load and validation process")
    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    blobs = list(bucket_obj.list_blobs(prefix=file_path))
    csv_blobs = [blob for blob in blobs if blob.name.endswith(".csv")]

    if not csv_blobs:
        logger.warning("No CSV files found in the specified directory.")
        return

    engine = create_engine(db_url)
    create_table(engine)

    for blob in csv_blobs:
        logger.info(f"Processing file: {blob.name}")
        try:
            df = download_csv(bucket, blob.name)
            report = validate_dataframe(df, blob.name)
            upload_report(bucket, report, blob.name)
            upload_html_report(report, blob.name)

            df = prepare_dataframe(df, blob.name)
            load_to_postgres(df, engine)
            logger.info(f"File loaded and validated: {blob.name}")
        except Exception as e:
            logger.error(f"Error processing {blob.name}: {e}")

    logger.info("Data load and validation process completed.")


if __name__ == "__main__":
    main()
