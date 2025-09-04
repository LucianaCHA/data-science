import os

from pydantic import BaseModel


class Settings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "database")
    DB_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    DB_NAME: str = os.getenv("POSTGRES_DB", "NOT_SET")
    DB_USER: str = os.getenv("POSTGRES_USER", "NOT_SET")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "NOT_SET")
    DB_CONNECTION_NAME: str = os.getenv("CONNECTION_NAME", "NOT_SET")
    DB_URL: str = os.getenv("DB_URL", "NOT_SET")
    GCS_BUCKET: str = os.getenv("GCS_BUCKET", "pi-mod03")
    GCS_FILE_PATH: str = os.getenv("GCS_FILE_PATH", "raw/data/airbnb/")
    DBT_PROJECT_DIR: str = os.getenv("DBT_PROJECT_PATH", "/")
    DBT_PROFILES_DIR: str = os.getenv("DBT_PROFILES_DIR", "/dbt_project/")
