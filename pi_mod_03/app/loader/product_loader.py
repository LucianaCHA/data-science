import re
from app.models.products import Product
from app.loader.base import DataLoader
from app.loader.constants import SQL_TO_PRODUCT_MODEL
from app.models.constants import TableNames
from app.utils.loader_utils import LoaderTablesPriority, LoaderSQLFilePaths


class UserLoader(DataLoader):
    priority = LoaderTablesPriority.PRODUCTS
    sql_to_model = SQL_TO_PRODUCT_MODEL
    file_path = LoaderSQLFilePaths.PRODUCTS
    table_name = TableNames.PRODUCTS

    def _parse_file(self, content: str) -> list[dict]:
        # Eliminar "USE ..." y "GO"
        content = re.sub(r"(?i)USE\s+\w+;", "", content)
        content = re.sub(r"(?i)\bGO\b", "", content)

        # Buscar todos los bloques INSERT INTO Productos (...) VALUES (...);
        pattern = r"INSERT INTO Productos\s*\((.*?)\)\s*VALUES\s*(.*?);"
        matches = re.findall(pattern, content, re.DOTALL)

        records = []
        for columns_str, values_block in matches:
            # Parsear columnas
            columns = [col.strip() for col in columns_str.split(",")]

            # Separar múltiples tuplas de valores
            value_tuples = re.findall(r"\((.*?)\)", values_block, re.DOTALL)

            for val_str in value_tuples:
                raw_values = [v.strip().strip("'") for v in re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", val_str)]

                if len(raw_values) != len(columns):
                    continue

                record = {
                    self.sql_to_model.get(col, col).lower(): val
                    for col, val in zip(columns, raw_values)
                }

                # Casteo
                for key, value in record.items():
                    if value.replace(".", "", 1).isdigit():
                        record[key] = float(value) if "." in value else int(value)

                records.append(record)

        return records

    def _save_records(self, db, records):
        products = [Product.from_dict(rec) for rec in records]
        try:
            db.bulk_save_objects(products)
            db.commit()
            print(
                f"{len(products)} products creados correctamente de un total de {len(records)}."
            )
        except Exception as e:
            db.rollback()
            print(f"Error al guardar products: {e}")
