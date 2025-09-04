from app.db.session import get_db
from app.models.data_loads import DataLoad
from app.models.data_loader import CSVLoader
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.services.logger.gcloud_logger import CloudLogger


logger = CloudLogger()


class DataLoadService(DataLoad):
    """
    Service class for handling data load operations and audit logging.
    """

    def __init__(self):
        pass

    def is_file_already_loaded(self, db: Session, file_name: str) -> bool:
        """ Checks if a file with the same name has already been loaded."""
        result = (
            db.query(DataLoad)
            .filter(
                and_(DataLoad.file_name == file_name, DataLoad.status == "successful")
            )
            .order_by(DataLoad.load_timestamp.desc())
            .first()
        )
        return result is not None

    def register_load(self, db: Session, file_name: str, status: str = "successful"):
        """Registers a load attempt in the audit table."""
        try:
            data_load = DataLoad(file_name=file_name, status=status)
            db.add(data_load)
            db.commit()
            logger.info(f"Registro de carga insertado para el archivo {file_name}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error al insertar el registro de carga: {e}")
            raise

    def load_csv_to_db(self, file_path: str, table_name: str):
        """Carga los datos de un archivo CSV usando CSVLoader"""
        db = next(get_db())
        try:
            loader = CSVLoader(file_path, table_name)
            loader.load(db)
        except Exception as e:
            logger.error(f"Fallo al cargar CSV {file_path}: {e}")
            raise
        finally:
            db.close()
