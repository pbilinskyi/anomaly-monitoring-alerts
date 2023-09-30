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


def update_google_sheets_table(df: pd.DataFrame,
                               sheet_name: str):
    """ Updates a Google Sheet by appending a dataframe to it.
    """
    logging.info('Updating Google Sheet...')

    df['Datetime'] = str(datetime.datetime.now())
    worksheet = connect_to_google_sheet(sheet_name)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    logging.info('SUCCESS: Google Sheet updated.')
