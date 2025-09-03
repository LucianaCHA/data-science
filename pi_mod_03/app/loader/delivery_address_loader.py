from app.loader.constants import SQL_TO_DELIVERY_ADDRESS_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.delivery_addresses import DeliveryAddress
from app.loader.base import DataLoader


class DeliveryAddressLoader(DataLoader):
    priority = LoaderTablesPriority.DELIVERY_ADDRESS
    sql_to_model = SQL_TO_DELIVERY_ADDRESS_MODEL
    file_path = LoaderSQLFilePaths.DELIVERY_ADDRESS
    table_name = TableNames.DELIVERY_ADDRESS

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract delivery address records."""
        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        delivery_addresses = [DeliveryAddress.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(delivery_addresses)
            db.commit()
            print(
                f"{len(delivery_addresses)} direcciones de entrega creadas correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar direcciones de entrega: {e}")
