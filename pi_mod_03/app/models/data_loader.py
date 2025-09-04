import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.logger.gcloud_logger import CloudLogger


logger = CloudLogger()


class CSVLoader:
    """
    Class to load CSV files into a table and log the load in audit table.
    """

    def __init__(self, file_path, table_name):
        self.file_path = file_path
        self.table_name = table_name

    def load(self, db: Session):
        """Loads the CSV file into database if it has not been loaded."""
        if self.is_file_already_loaded(db, self.file_path):
            logger.info(f"file {self.file_path} already loaded. Skipping...")
            return

        try:

            df = pd.read_csv(self.file_path)
            logger.info(f"CSV loaded successfully from {self.file_path}")

            self.insert_to_db(df, db)

            self.insert_load_record(db)

        except Exception as e:
            logger.error(f"Error loading and inserting CSV file: {e}")
            raise

    def insert_to_db(self, df: pd.DataFrame, db: Session):
        """Insert the DataFrame into the database using the session."""
        try:
            df.to_sql(self.table_name, con=db.bind, index=False, if_exists="replace")

            logger.info(f"Data successfully inserted table {self.table_name}")
        except Exception as e:

            logger.error(f"Error inserting data into the database: {e}")
            raise

    def insert_load_record(self, db: Session):
        """Registers in the audit table that this file was loaded."""
        try:
            db.execute(
                text(
                    "INSERT INTO data_loads_audit (file_name, status) VALUES (:file_name, :status)"
                ),
                {"file_name": self.file_path, "status": "successful"},
            )
            db.commit()
            print(f"Registro de carga insertado para el archivo {self.file_path}")
        except Exception as e:
            logger.error(f"Error registering load audit: {e}")
            db.rollback()
            raise

    def is_file_already_loaded(self, db: Session, file_name: str):
        """ Checks if a file with the same name has already been loaded."""
        result = db.execute(
            text(
                "SELECT * FROM data_loads_audit WHERE file_name = :file_name AND status = 'successful' ORDER BY load_timestamp DESC LIMIT 1"
            ),
            {"file_name": file_name},
        )
        return result.first() is not None
