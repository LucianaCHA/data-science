import pandas as pd

def print_rows (rows):
    """
    Print the rows in a formatted way.
    """
    for row in rows:
        print(row)

def print_query_results(connection, query):
    """
    Execute a query and print the results.
    """
    data_frame = pd.read_sql_query(query, connection)

    print(data_frame)

def show_query_results(connection, query, limit=None):
    """
    Show the results of a query.
    """
    data = pd.read_sql_query(query, connection )
    data.head(limit) if limit else data.head()
