from abc import ABC
import csv
import re
from sqlalchemy.orm import Session
from typing import List, Dict
from app.models.constants import TableNames
from app.utils.loader_utils import (
    LoaderInsertFormat,
    LoaderRegexPatterns,
    LoaderSQLFilePaths,
    LoaderTablesPriority,
)
from io import StringIO


class DataLoader(ABC):  # Abstract Base Clas
    _registry = []
    priority: LoaderTablesPriority = 100
    file_path: LoaderSQLFilePaths = ""
    sql_to_model: Dict[str, str] = {}
    table_name: TableNames = ""

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        DataLoader._registry.append(cls)

    def _read_file(self) -> str:
        with open(self.file_path, "r") as file:
            print(f"Reading file: {self.file_path}")
            return file.read()

    def _parse_file(self) -> List[Dict]:
        """should be overridden by each loader to parse the file content
        and return a list of dictionaries representing the records to save."""
        raise NotImplementedError

    def _save_records(self, db: Session, records: List[Dict]):
        """should be overridden by each loader to save the parsed records"""
        raise NotImplementedError

    def _get_table_regex_pattern(self) -> str:
        # """Returns a regex pattern to match SQL INSERT statements for the specific table."""
        # return rf"INSERT INTO {self.table_name} .*?VALUES \((.*?)\);"
        return LoaderRegexPatterns.get(self.table_name)

    def _handle_insert_from_sql(
        self,
        content: str,
        table_name: str,
        sql_to_model: Dict[str, str],
        extra_fields: Dict[str, any] = None,
    ) -> List[Dict]:
        """
        Extrae registros de sentencias SQL INSERT a partir del contenido
        de un archivo .sql y los convierte en diccionarios según el mapeo sql_to_model.
        """

        # Obtener el patrón de regex y el tipo de formato (SINGLE_LINE o MULTI_LINE)
        pattern, format_type = LoaderRegexPatterns.get(table_name)

        records = []

        if format_type == LoaderInsertFormat.SINGLE_LINE:
            # MATCH para líneas como: INSERT INTO tabla (...) VALUES ('a', 'b', 1, 2);
            matches = pattern.findall(content)

            for values_str in matches:
                # Usa csv.reader para dividir los valores con comas internas correctamente
                reader = csv.reader(
                    StringIO(values_str), quotechar="'", skipinitialspace=True
                )
                for row in reader:
                    if len(row) != len(sql_to_model):
                        continue

                    # Construir el diccionario usando el mapeo
                    record = {
                        sql_to_model[col]: row[i] for i, col in enumerate(sql_to_model)
                    }
                    print(f"Parsed record: {record}")
                    if extra_fields:
                        record.update(extra_fields)
                    records.append(record)

        elif format_type == LoaderInsertFormat.MULTI_LINE:
            # MATCH para múltiples tuplas: INSERT INTO tabla (...) VALUES (...), (...), (...);
            match = pattern.search(content)
            if not match:
                print(f" No se encontró un INSERT válido para {table_name}.")
                return []

            # Extraer columnas y el bloque de valores
            columns_str, values_block = match.groups()
            # columns = [col.strip() for col in columns_str.split(",")]
            columns = [col.strip() for col in columns_str.split(",")]

            # Validar que todas las columnas existan en sql_to_model
            mapped_columns = [sql_to_model.get(col) for col in columns]
            if None in mapped_columns:
                raise ValueError(
                    f"Algunas columnas no están en sql_to_model: {columns}"
                )

            # Extraer cada tupla: (…), (…), … — incluso con saltos de línea y comas internas
            value_tuples = re.findall(r"\((.*?)\)", values_block, re.DOTALL)

            for tpl in value_tuples:
                reader = csv.reader(StringIO(tpl), quotechar="'", skipinitialspace=True)
                for row in reader:
                    if len(row) != len(mapped_columns):
                        print(
                            f" Column/value mismatch: columns={columns} vs values={row}"
                        )
                        continue

                    record = {mapped_columns[i]: row[i] for i in range(len(row))}
                    if extra_fields:
                        record.update(extra_fields)
                    records.append(record)

        else:
            raise ValueError(f" Unknown insert format type: {format_type}")

        return records

    def run(self, db: Session):
        content = self._read_file()
        print(f"Processing file: {self.file_path}")
        records = self._parse_file(content)
        print(f"Parsed {len(records)} records from {self.file_path}.")
        self._save_records(db, records)
