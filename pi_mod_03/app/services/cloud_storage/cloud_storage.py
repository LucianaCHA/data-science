from google.cloud import storage
from app.services.filename_handler import FilenameHandler, file_extension, frequency
from datetime import datetime
from typing import Optional


class GCSService:
    def __init__(self, bucket_name: str):
        """Inicializa el servicio de Google Cloud Storage."""
        self.bucket_name = bucket_name
        self.storage_client = storage.Client()

    def _get_bucket(self):
        """Obtiene el bucket de GCS."""
        try:
            return self.storage_client.get_bucket(self.bucket_name)
        except Exception as e:
            print(f"Error al acceder al bucket: {e}")
            return None

    def upload_file(
        self, file_content: str, file_path: str, content_type: str = "application/json"
    ):
        """Sube un archivo a GCS."""
        bucket = self._get_bucket()
        if not bucket:
            return

        try:
            # Crear un blob (archivo) en el bucket
            blob = bucket.blob(file_path)

            # Subir el archivo
            blob.upload_from_string(file_content, content_type=content_type)
            print(f"Archivo guardado en: gs://{self.bucket_name}/{file_path}")
        except Exception as e:
            print(f"Error al subir el archivo a GCS: {e}")

    def download_file(self, blob_name: str) -> str:
        """Descarga un archivo de GCS y retorna su contenido."""
        bucket = self._get_bucket()
        if not bucket:
            return None

        try:
            blob = bucket.blob(blob_name)
            content = blob.download_as_text()
            return content
        except Exception as e:
            print(f"Error al descargar el archivo: {e}")
            return None

    def generate_filename(
        self,
        source: str,
        dataset: str,
        extension: file_extension,
        date: Optional[datetime] = None,
    ) -> str:
        """Genera un nombre de archivo basado en un patrón determinado."""
        return FilenameHandler._create(
            source=source,
            dataset=dataset,
            frequency=frequency.DAILY,
            extension=extension,
            date=date or datetime.now(),
        )

    def list_blobs(self, prefix: str = ""):
        """Lista los blobs en el bucket que comienzan con el prefijo dado."""
        try:
            bucket = self._get_bucket()
            blobs = bucket.list_blobs(prefix=prefix)
            return blobs
        except Exception as e:
            print(f"Error al listar los blobs en el bucket: {e}")
            return []

    def get_file_size(self, file_name: str) -> int:
        """Obtiene el tamaño de un archivo en bytes."""
        bucket = self._get_bucket()
        if not bucket:
            return 0

        try:
            blob = bucket.blob(file_name)
            blob.reload()  
            return blob.size
        except Exception as e:
            print(f"Error al obtener el tamaño del archivo: {e}")
            return 0
