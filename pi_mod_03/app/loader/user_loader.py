from datetime import datetime
from app.models.users import User
from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_USER_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderTablesPriority, LoaderSQLFilePaths


class UserLoader(DataLoader):
    priority = LoaderTablesPriority.USERS
    sql_to_model = SQL_TO_USER_MODEL
    file_path = LoaderSQLFilePaths.USERS
    table_name = TableNames.USERS

    def _parse_file(self, content: str) -> list[dict]:
        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
            extra_fields={"registration_date": datetime.now()},
        )

    def _save_records(self, db, records):
        users = [User.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(users)
            db.commit()
            print(
                f"{len(users)} usuarios creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar usuarios: {e}")
