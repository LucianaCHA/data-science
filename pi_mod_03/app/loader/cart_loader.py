from app.loader.constants import SQL_TO_CART_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.cart import Cart
from app.loader.base import DataLoader


class DeliveryAddressLoader(DataLoader):
    priority = LoaderTablesPriority.CART
    sql_to_model = SQL_TO_CART_MODEL
    file_path = LoaderSQLFilePaths.CART
    table_name = TableNames.CART

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract delivery address records."""
        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        carts = [Cart.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(carts)
            db.commit()
            print(
                f"{len(carts)} carritos creadas correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar direcciones de entrega: {e}")
