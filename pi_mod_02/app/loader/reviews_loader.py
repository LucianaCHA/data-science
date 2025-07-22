from datetime import datetime
from app.models.reviews import ProductReview
from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_PRODUCT_REVIEW_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderTablesPriority, LoaderSQLFilePaths


class ReviewLoader(DataLoader):
    priority = LoaderTablesPriority.REVIEWS
    sql_to_model = SQL_TO_PRODUCT_REVIEW_MODEL
    file_path = LoaderSQLFilePaths.REVIEWS
    table_name = TableNames.REVIEWS

    def _parse_file(self, content: str) -> list[dict]:
        return self._handle_insert_from_sql(
            content,
            table_name=self.table_name,
            sql_to_model=self.sql_to_model,
            extra_fields={"date": datetime.now()},
        )

    def _save_records(self, db, records):
        reviews = [ProductReview.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(reviews)
            db.commit()
            print(
                f"{len(reviews)} reviews creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar reviews: {e}")