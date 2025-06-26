
from utils.postgres_utils import connect_to_db, run_non_select_query


class BaseModel:
    table = None
    fields = [] 

    @classmethod
    def to_dict(cls, values: tuple | list):
        """
        Turn a tuple or list of values into a dictionary
        where keys are the field names defined in the model.
        """
        if len(values) != len(cls.fields):
            raise ValueError(f"{cls.__name__}: Mismatch between values and fields. ")
        
        return dict(zip(cls.fields, values))
    
    @classmethod
    def set_from_rows(cls, rows: list[tuple | list]):
        """
        Set the model's attributes from a list of rows.
        Each row is a tuple or list of values corresponding to the model's fields.
        """
        if not rows:
            return
        
        if len(rows[0]) != len(cls.fields):
            raise ValueError(f"{cls.__name__}: Mismatch between row length and fields. ")
        
        return [cls.to_dict(row) for row in rows]
    
    @classmethod
    def insert(cls, **kwargs):
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        values = tuple(kwargs.values())

        query = f"INSERT INTO {cls.table} ({columns}) VALUES ({placeholders})"

        try:

            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            cur.close()
            conn.close()
            print(f"{cls.__name__} inserted successfully.")
        except Exception as error:
            print(f"Error inserting {cls.__name__}: {e}")
            raise error

    @classmethod
    def bulk_insert(cls, records: list[dict]):
        if not records:
            return
        columns = ', '.join(records[0].keys())
        placeholders = ', '.join(['%s'] * len(records[0]))
        values = [tuple(r.values()) for r in records]

        query = f"INSERT INTO {cls.table} ({columns}) VALUES ({placeholders})"

        try:

            conn = connect_to_db()
            cur = conn.cursor()
            cur.executemany(query, values)
            conn.commit()
            cur.close()
            conn.close()

            print(f"{cls.__name__} bulk inserted successfully.")
        except Exception as error:
            print(f"Error bulk inserting {cls.__name__}: {error}")
            raise error


    @classmethod
    def delete(cls, **kwargs):
        if not kwargs:
            raise ValueError("No conditions provided for deletion.")

        conditions = ' AND '.join([f"{k} = %s" for k in kwargs.keys()])
        values = tuple(kwargs.values())

        query = f"DELETE FROM {cls.table} WHERE {conditions}"

        try:

            conn = connect_to_db()
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            cur.close()
            conn.close()

            print(f"{cls.__name__} deleted successfully.")
        except Exception as error:
            print(f"Error deleting {cls.__name__}: {error}")
            raise error
        
    @classmethod
    def create_index(cls, index_name: str, columns: list[str]):
        if not isinstance(columns, list) or not all(isinstance(col, str) for col in columns):
            raise ValueError("Columns must be a list of strings.")
        if not index_name or not columns:
            raise ValueError("Index name and columns must be provided.")
        
        if not index_name.isidentifier():
            raise ValueError("Invalid index name.")

        for col in columns:
            if not col.isidentifier():
                raise ValueError(f"Invalid column name: {col}")

        columns_str = ', '.join(columns)
        query = f"CREATE INDEX IF NOT EXISTS {index_name} ON {cls.table} ({columns_str});"

        try:
            run_non_select_query(query)
            print(f"Index '{index_name}' created successfully on '{cls.table}'.")
        except Exception as error:
            print(f"Error creating index '{index_name}': {error}")
            raise