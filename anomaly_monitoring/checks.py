import logging

import pandas as pd

from .database_io import read_sql_query
from .slack_io import send_alert_slack
from .utils import dataframe_to_str


class AnomalyChecker:
    """Base class for anomaly checks, which use SQL queries.
    """

    def __init__(self, sql_query: str,
                 alert_message_template: str) -> None:
        self.sql_query = sql_query
        self.alert_message_template = alert_message_template

    def run_check(self):
        df_result = read_sql_query(self.sql_query)
        is_check_passed = self._is_valid_query_result(df_result)

        if is_check_passed:
            logging.info(f'[PASSED] Query result is valid: {df_result}')
        else:
            logging.info('[FAILED] Query result is NOT valid.'
                         'Sending alert...')
            self._send_alert(df_result)

    def _send_alert(self, df_result: pd.DataFrame) -> None:
        pass

    def _is_valid_query_result(self, df_result: pd.DataFrame) -> bool:
        pass

    def _create_alert_message(self, df_result: pd.DataFrame) -> str:
        pass


class QueryEmptyChecker(AnomalyChecker):
    """Check if the query result is empty (empty is good).
       Use cases:
           - Looking for anomalies with SQL query.
             If query result is empty, then no anomalies were detected.
             If it's not empty, it will contain info about detected anomalies.
    """

    def __init__(self, sql_query: str,
                 alert_message_template: str) -> None:
        super().__init__(sql_query, alert_message_template)

    def _send_alert(self, df_result: pd.DataFrame) -> None:
        slack_message_text = self._create_alert_message(df_result)
        send_alert_slack(slack_message_text)

    def _is_valid_query_result(self, df_result: pd.DataFrame) -> bool:
        return len(df_result) == 0

    def _create_alert_message(self, df_result: pd.DataFrame) -> str:
        text = self.alert_message_template.format(
            query_result=dataframe_to_str(df_result)
        )
        return text
