import traceback
from typing import Optional

from app.services.currency_api import ExchangeRateService
from app.raw.scripts.load_csvs import CSVLoaderService

from app.services.logger.gcloud_logger import CloudLogger

logger = CloudLogger()


def run_exchange_rates(bucket_name: Optional[str] = None):
    """Downloads and saves exchange rates in raw/exchange"""
    try:
        logger.info("Consulting USD exchange rate...")
        service = ExchangeRateService(
            base_url="https://dolarapi.com", bucket_name=bucket_name
        )
        service.get_exchange_rates()
        logger.info("Today's exchange rate saved in raw/exchange")
    except Exception as e:
        logger.error(f"Error while fetching exchange rate: {e}")
        logger.error(traceback.format_exc())


def run_csvs(bucket_name: Optional[str] = None):
    """Loads CSVs from GCS to the Data Lake with versioned names"""
    if not bucket_name:
        logger.warning("No bucket_name provided, skipping CSV loading.")
        return
    try:
        logger.info("Loading CSV files from GCS...")
        csv_loader = CSVLoaderService(bucket_name=bucket_name)
        csv_loader.load_csvs(destination_path="raw/data/airbnb")
        logger.info("CSV files saved in the Data Lake.")
    except Exception as e:
        logger.error(f"Error while loading CSVs: {e}")
        logger.error(traceback.format_exc())


def main():
    BUCKET_NAME = "pi-mod03"
    logger.info("=== Starting data integration in RAW layer ===")
    run_exchange_rates(bucket_name=BUCKET_NAME)
    run_csvs(bucket_name=BUCKET_NAME)
    logger.info("=== Integration completed ===")


if __name__ == "__main__":
    main()
