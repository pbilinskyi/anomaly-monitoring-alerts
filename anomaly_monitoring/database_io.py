import os

import pandas as pd
import duckdb


def open_conn() -> duckdb.DuckDBPyConnection:
    '''
    Opens a connection to the Data Warehouse database,
    which is a DuckDB database.

    Returns:
        duckdb.DuckDBPyConnection: A connection instance.

    Example:
        >>> con = open_conn()
        >>> con.execute("SELECT * FROM countries LIMIT 5;").fetchdf()
    '''
    con = duckdb.connect(os.path.join('data', 'dwh.db'))
    return con


def read_sql_query(query: str) -> pd.DataFrame:
    ''' Executes a SQL query from the DWH database
        and returns a result as pandas DataFrame.

    Args:
        query (str): A SQL query.

    Returns:
        pd.DataFrame: A pandas DataFrame.

    Example:
        >>> query = "SELECT * FROM countries LIMIT 5;"
        >>> df = read_sql_query(query)
    '''
    con = open_conn()
    try:
        df = con.execute(query).fetch_df()
        con.close()
    except Exception as e:
        con.close()
        raise e
    return df


def create_database():
    open_conn().close()
