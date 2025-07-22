from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_CATEGORY_MODEL
from app.utils.loader_utils import LoaderSQLFilePaths, LoaderTablesPriority
from app.models.constants import TableNames
from app.models.categories import Category


class CategoryLoader(DataLoader):
    priority = LoaderTablesPriority.CATEGORIES
    sql_to_model = SQL_TO_CATEGORY_MODEL
    file_path = LoaderSQLFilePaths.CATEGORIES
    table_name = TableNames.CATEGORIES

    def _parse_file(self, content: str) -> list[dict]:
        """Parses the SQL file content to extract category records."""

        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
        )

    def _save_records(self, db, records):
        categories = [Category.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(categories)
            db.commit()
            print(
                f"{len(categories)} categorias creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar usuarios: {e}")
