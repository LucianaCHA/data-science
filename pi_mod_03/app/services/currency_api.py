import os
import json
from datetime import datetime
from typing import List, Optional

from app.services.filename_handler import FilenameHandler, file_extension, frequency
from app.services.cloud_storage.cloud_storage import GCSService
from app.services.validations_service import validate_file_in_gcs
from scripts.extraction.use_api import APIClient
from app.services.logger.gcloud_logger import CloudLogger

logger = CloudLogger()

SOURCE = "dolarapi"
DATASET = "exchange"
ENDPOINT = "v1/dolares"
CACHE_KEY = "exchange_rates"
GCS_PATH = "raw/data/exchange"
RAW_DIR = "/app/raw/data/exchange/"


class ExchangeRateService:
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        bucket_name: Optional[str] = None,
    ):
        self.api_client = APIClient(base_url, api_key)
        self.bucket_name = bucket_name

        self.storage_client = (
            GCSService(bucket_name).storage_client if bucket_name else None
        )

        self.filename = FilenameHandler._create(
            source=SOURCE,
            dataset=DATASET,
            frequency=frequency.DAILY,
            extension=file_extension.JSON,
            date=datetime.now(),
        )

    def get_exchange_rates(self, date: Optional[str] = None) -> List[dict]:
        params = {}
        endpoint = ENDPOINT
        cache_key = f"{CACHE_KEY}_{date or 'today'}"

        data = self.api_client.fetch_data(endpoint, params, cache_key)

        if data:
            logger.info(f"Datos obtenidos: {data}")
            self.save_exchange_rates(data)
            return data
        else:
            return []

    def _save_to_raw(self, data: List[dict]):
        os.makedirs(RAW_DIR, exist_ok=True)

        filepath = os.path.join(RAW_DIR, self.filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"Cotización guardada en: {filepath}")

    def _save_to_cloud(self, data: List[dict]):

        file_content = json.dumps(data, ensure_ascii=False, indent=2)

        try:
            bucket = self.storage_client.get_bucket(self.bucket_name)

        except Exception as e:
            logger.error(f"Error al acceder al bucket: {e}")
            return

        blob = bucket.blob(f"{GCS_PATH}/{self.filename}")

        blob.upload_from_string(file_content, content_type="application/json")

        validate_file_in_gcs(self.bucket_name, f"{GCS_PATH}/{self.filename}")

    def save_exchange_rates(self, data: List[dict]):

        if self.bucket_name and self.storage_client:
            self._save_to_cloud(data)
        else:
            self._save_to_raw(data)
