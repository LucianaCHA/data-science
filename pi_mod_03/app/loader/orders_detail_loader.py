from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_ORDER_DETAIL_MODEL
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.constants import TableNames
from app.models.orders_detail import OrderDetail


class OrderDetailLoader(DataLoader):
    priority = LoaderTablesPriority.ORDER_DETAIL
    sql_to_model = SQL_TO_ORDER_DETAIL_MODEL
    file_path = LoaderSQLFilePaths.ORDERS_DETAIL
    table_name = TableNames.ORDER_DETAILS

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract category records."""

        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        orders = [OrderDetail.from_dict(rec) for rec in records]

        try:
            db.bulk_save_objects(orders)
            db.commit()
            print(
                f"{len(orders)} orders detail creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar detalle de ordene : {e}")