import traceback
from app.services.cloud_storage.cloud_storage import GCSService
from app.services.logger.gcloud_logger import CloudLogger

logger = CloudLogger()


def validate_file_in_gcs(bucket_name: str, file_name: str, min_size: int = 1):
    """Validates if a file exists in GCS and meets minimum size requirements."""
    try:
        storage_client = GCSService(bucket_name).storage_client
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)

        blob.reload()

        if not blob.exists():
            logger.error(
                f"The file {file_name} does not exist in bucket {bucket_name}."
            )
            return False

        # Check the minimum file size (in bytes)
        file_size = blob.size
        print(f"File size of {file_name}: {file_size} bytes")
        logger.info(f"File size of {file_name}: {file_size} bytes")
        if file_size < min_size:
            logger.error(
                f"The file {file_name} is too small (size: {file_size} bytes)."
            )
            return False

        logger.info(
            f"File {file_name} validated successfully. Size: {file_size} bytes."
        )
        return True

    except Exception as e:
        logger.error(f"Error validating file {file_name}: {e}")
        traceback.print_exc()
        return False
