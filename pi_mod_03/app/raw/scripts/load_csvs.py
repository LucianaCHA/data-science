from app.services.cloud_storage.cloud_storage import GCSService
from app.services.filename_handler import file_extension
from app.services.validations_service import validate_file_in_gcs
from app.services.logger.gcloud_logger import CloudLogger

logger = CloudLogger()


class CSVLoaderService:
    def __init__(self, bucket_name: str, source: str = "csv_loader"):
        """Initializes the CSV loading service."""
        self.gcs_service = GCSService(bucket_name=bucket_name)
        self.source = source

    def _process_and_upload(self, filename: str, destination_path: str):
        """Processes and uploads the CSV file to GCS."""
        file_content = self._download_csv(filename)
        if file_content:
            new_filename = self.gcs_service.generate_filename(
                source=self.source, dataset="csv_data", extension=file_extension.CSV
            )

            # Upload the renamed file to the Data Lake
            self.gcs_service.upload_file(
                file_content,
                f"{destination_path}/{new_filename}",
                content_type="text/csv",
            )
            validate_file_in_gcs(
                bucket_name=self.gcs_service.bucket_name,
                file_name=f"{destination_path}/{new_filename}",
            )
        else:
            logger.error(f"Error processing file {filename}")

    def _download_csv(self, filename: str) -> str:
        """Downloads the CSV file from the GCS bucket."""
        try:
            # file_path = f"{filename}"
            return self.gcs_service.download_file(blob_name=filename)
        except Exception as e:
            logger.error(f"Error downloading file {filename} from GCS: {e}")
            return None

    def load_csvs(self, destination_path: str):
        """Loads all CSV files from GCS to a versioned destination in the Data Lake."""
        try:
            blobs = self.gcs_service.list_blobs(prefix="data/")

            csv_files = [blob.name for blob in blobs if blob.name.endswith(".csv")]

            for csv_file in csv_files:
                logger.info(f"Starting upload for file: {csv_file}")
                self._process_and_upload(csv_file, destination_path)

            logger.info("CSV file upload completed.")
        except Exception as e:
            logger.error(f"Error loading CSVs: {e}")
