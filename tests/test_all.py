from anomaly_monitoring.database_io import read_sql_query
from anomaly_monitoring.utils import quote_str


def test_is_data_available():
    ''' Tests if all required tables exist in the database
        and are nonempty.
    '''
    table_names = ['countries',
                   'orders',
                   'test_aggregate_data',
                   'transactions']

    for table_name in table_names:
        # 1. check if table exists
        query_is_exists = f"""
            select *
            from information_schema.tables
            where table_name = '{table_name}';
        """
        df_result = read_sql_query(query_is_exists)
        assert len(df_result) > 0, \
               f'Table {quote_str(table_name)} does not exist in the database.'

        # 2. check if table is nonempty
        query_is_nonempty = f'select 1 from {table_name} limit 1;'
        df_result = read_sql_query(query_is_nonempty)
        assert len(df_result) > 0, f'Table {table_name} is empty.'
