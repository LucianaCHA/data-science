import os

from pydantic import BaseModel


class Settings(BaseModel):
    DB_HOST: str = os.getenv("DB_HOST", "database")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "airbnb-db")
    DB_USER: str = os.getenv("DB_USER", "lu")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "lu")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DBT_PROJECT_DIR: str = os.getenv("DBT_PROJECT_PATH", "/")
    DBT_PROFILES_DIR: str = os.getenv("DBT_PROFILES_DIR", "/dbt_project/")
