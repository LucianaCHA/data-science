import os
import time
import json
import requests
from requests.exceptions import RequestException, Timeout


class APIClient:
    def __init__(self, base_url, api_key=None, retries=3, timeout=10, cache_ttl=3600):
        """
        :param base_url: URL base de la API
        :param api_key: API Key si aplica
        :param retries: Número de reintentos
        :param timeout: Timeout de la request
        :param cache_ttl: Tiempo de validez del caché en segundos
        """
        self.base_url = base_url
        self.api_key = api_key
        self.retries = retries
        self.timeout = timeout
        self.cache_ttl = cache_ttl

        self.cache_dir = "/app/app/raw/data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, cache_key):
        return os.path.join(self.cache_dir, f"{cache_key}.json")

    def _load_cache(self, cache_key):
        cache_path = self._get_cache_path(cache_key)
        if os.path.exists(cache_path):
            # Verificar si está vigente
            if (time.time() - os.path.getmtime(cache_path)) < self.cache_ttl:
                with open(cache_path, "r", encoding="utf-8") as f:
                    print(f"recuperando datos desde caché: {cache_key}")
                    return json.load(f)
        return None

    def _save_cache(self, cache_key, data):
        cache_path = self._get_cache_path(cache_key)
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _make_request(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}/{endpoint}"
        if not headers:
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None
        except Timeout:
            print(f" Tiempo de espera agotado ({self.timeout} seg).")
            return None

    def fetch_data(self, endpoint, params=None, cache_key=None):
        """
        Obtiene datos desde la API con caché.
        """
        if cache_key:
            cached_data = self._load_cache(cache_key)
            if cached_data:
                return cached_data

        for attempt in range(self.retries):
            data = self._make_request(endpoint, params)
            if data:
                if cache_key:
                    self._save_cache(cache_key, data)
                print(f"Datos obtenidos correctamente de {endpoint}.")
                return data
            print(f" Intento {attempt + 1} fallido. Reintentando en 3 segundos...")
            time.sleep(3)

        print(f"No se pudieron obtener datos de {endpoint} después de {self.retries} intentos.")
        return None
