from datetime import datetime
from enum import StrEnum
from app.utils.date_utils import NOW


class frequency(StrEnum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"


class file_extension(StrEnum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    XML = "xml"
    TXT = "txt"


class FilenameHandler:

    @staticmethod
    def _set_time_format(freq: frequency) -> str:
        formats = {
            frequency.HOURLY: "%Y_%m_%d_%H",
            frequency.DAILY: "%Y_%m_%d",
            frequency.WEEKLY: "%Y_%W",
            frequency.MONTHLY: "%Y_%m",
        }
        return formats.get(freq, "%Y_%m_%d")

    @staticmethod
    def _create(
        source: str,
        dataset: str,
        frequency: frequency = frequency.ON_DEMAND,
        extension: file_extension = file_extension.JSON,
        date: datetime = None,
        location: str = None,
        extra: str = None,
    ) -> str:
        """
        Creates a consistent filename for raw data.
        """
        if date is None:
            date = NOW
        date_str = date.strftime(FilenameHandler._set_time_format(frequency))

        parts = [source, dataset, frequency.value]
        if location:
            parts.append(location)
        if extra:
            parts.append(extra)
        parts.append(date_str)

        filename = "_".join(parts) + f".{extension.value}"
        return filename
