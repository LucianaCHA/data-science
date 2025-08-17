import os

from pydantic import BaseModel


class Settings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "ecommerce")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")

    DBT_PROJECT_DIR: str = os.getenv("DBT_PROJECT_PATH", "/")
    DBT_PROFILES_DIR: str = os.getenv("DBT_PROFILES_DIR", "/dbt_project/")
