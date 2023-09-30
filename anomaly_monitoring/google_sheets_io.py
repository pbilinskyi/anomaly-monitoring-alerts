import os
import datetime
import logging

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv


def connect_to_google_sheet(sheet_name: str):
    load_dotenv()

    scopes = ['https://www.googleapis.com/auth/spreadsheets',
              'https://www.googleapis.com/auth/drive']
    PATH_TO_CREDENTIALS = os.getenv('PATH_TO_GOOGLE_JSON_CREDENTIALS')
    credentials = Credentials.from_service_account_file(PATH_TO_CREDENTIALS,
                                                        scopes=scopes)
    gc = gspread.authorize(credentials)

    # open a google sheet
    SHEET_KEY = os.getenv('GOOGLE_SHEET_KEY')
    gs = gc.open_by_key(SHEET_KEY)
    worksheet = gs.worksheet(sheet_name)

    return worksheet


def update_google_sheets_table(df_to_append: pd.DataFrame,
                               sheet_name: str):
    """ Updates a Google Sheet by appending a dataframe to it.
    """
    logging.info('Updating Google Sheet...')

    worksheet = connect_to_google_sheet(sheet_name)
    df_existing = pd.DataFrame(worksheet.get_all_records())

    df_to_append.insert(column='Datetime',
                        value=str(datetime.datetime.now()),
                        loc=0)

    if set(df_existing.columns) != set(df_to_append.columns):
        raise ValueError(
              'Cannot append dataframe to Google Sheet,'
              'because it has different columns.\n'
              f'Columns in Google Sheet: \n{df_existing.columns.to_list()}\n'
              'Columns in dataframe to append: '
              f'\n{df_to_append.columns.to_list()}')

    df = pd.concat([df_existing, df_to_append], ignore_index=True)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    logging.info('SUCCESS: Google Sheet updated.')
