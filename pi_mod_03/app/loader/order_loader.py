from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_ORDER_MODEL
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.constants import TableNames
from app.models.orders import Order


class OrderLoader(DataLoader):
    priority = LoaderTablesPriority.ORDERS
    sql_to_model = SQL_TO_ORDER_MODEL
    file_path = LoaderSQLFilePaths.ORDERS
    table_name = TableNames.ORDERS

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract category records."""

        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        orders = [Order.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(orders)
            db.commit()
            print(
                f"{len(orders)} categorias creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar usuarios: {e}")