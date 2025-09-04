from asyncio import Timeout
from typing import Optional
import requests
import time
import json
import os
from app.services.logger.gcloud_logger import CloudLogger


logger = CloudLogger()


class APIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        retries: int = 3,
        timeout: int = 10,
        cache_file: str = "cache.json",
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.retries = retries
        self.timeout = timeout
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def save_cache(self):
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=4)

    def _make_request(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> Optional[dict]:
        url = f"{self.base_url}/{endpoint}"

        if headers:
            headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            logger.info(
                "Requesting data from API",
                extra={
                    "url": url,
                    "params": params,
                },
            )
            response = requests.get(
                url, params=params, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return None

        except Timeout:
            logger.error(f"Request to {url} timed out after " f"{self.timeout} seconds")

            return None

    def fetch_data(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        cache_key: Optional[str] = None,
    ) -> Optional[dict]:
        if cache_key and cache_key in self.cache:
            logger.info(f"Using cached data for {cache_key}")
            return self.cache[cache_key]

        for attempt in range(self.retries):
            data = self._make_request(endpoint, params)
            if data:
                if cache_key:
                    self.cache[cache_key] = data
                    self.save_cache()
                return data
            else:
                logger.warning(f"Attempt {attempt + 1} failed. Retrying...")
                time.sleep(3)

        return None
