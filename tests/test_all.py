import pandas as pd

from anomaly_monitoring.database_io import read_sql_query
from anomaly_monitoring.utils import quote_str
from anomaly_monitoring.google_sheets_io import (
    connect_to_google_sheet,
    update_google_sheets_table
)
from anomaly_monitoring.slack_io import connect_to_slack_client


def test_is_data_available():
    ''' Tests if all required tables exist in the database
        and are nonempty.
    '''
    table_names = ['orders',
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


def test_slack_auth():
    """ Tests if the connection to Slack is established.
    """
    client = connect_to_slack_client()
    response = client.auth_test()
    assert response.get("ok")


def test_google_sheet_auth():
    """ Tests if the connection to Google Sheets is established and working.
    """
    sheet_name = 'Anomaly: unfinished orders'
    worksheet = connect_to_google_sheet(sheet_name)
    assert worksheet is not None

    df_existing = pd.DataFrame(worksheet.get_all_records())
    assert df_existing is not None


def test_google_sheet_update():
    """ Tests if the Google Sheet update works.
    """
    df = pd.DataFrame({'Order ID': []})
    update_google_sheets_table(df, sheet_name='Anomaly: unfinished orders')
