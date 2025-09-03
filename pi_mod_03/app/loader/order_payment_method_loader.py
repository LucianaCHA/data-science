from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_ORDERS_PAYMENT_METHOD_MODEL
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.constants import TableNames
from app.models.order_payment_methods import OrderPaymentMethod


class OrderPaymentMethodLoader(DataLoader):
    priority = LoaderTablesPriority.ORDERS_PAYMENT_METHODS
    sql_to_model = SQL_TO_ORDERS_PAYMENT_METHOD_MODEL
    file_path = LoaderSQLFilePaths.ORDERS_PAYMENT_METHODS
    table_name = TableNames.ORDERS_PAYMENT_METHODS

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract category records."""

        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        orders = [OrderPaymentMethod.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(orders)
            db.commit()
            print(
                f"{len(orders)} orders methods creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar usuarios: {e}")
