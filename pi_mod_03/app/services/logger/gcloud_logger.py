import logging
from google.cloud import logging as cloud_logging
from google.cloud.logging.handlers import CloudLoggingHandler


class CloudLogger:
    def __init__(self, name="raw_data_logger", level=logging.INFO):
        # Inicializar cliente de Cloud Logging
        self.client = cloud_logging.Client()
        # Crear handler para enviar logs a Google Cloud Logging
        handler = CloudLoggingHandler(self.client)

        # Crear logger con el nombre dado y nivel configurado
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Evitar agregar múltiples handlers si ya tiene
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)
