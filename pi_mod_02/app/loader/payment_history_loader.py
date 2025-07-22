from app.loader.constants import SQL_TO_PRODUCT_PAYMENT_HISTORY_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.payment_history import PaymentHistory
from app.loader.base import DataLoader


class PaymentHistoryLoader(DataLoader):
    priority = LoaderTablesPriority.PAYMENT_HISTORY
    sql_to_model = SQL_TO_PRODUCT_PAYMENT_HISTORY_MODEL
    file_path = LoaderSQLFilePaths.PAYMENT_HISTORY
    table_name = TableNames.PAYMENT_HISTORY

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract delivery address records."""
        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        payments = [PaymentHistory.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(payments)
            db.commit()
            print(
                f"{len(payments)} payments creadas correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar direcciones de entrega: {e}")
