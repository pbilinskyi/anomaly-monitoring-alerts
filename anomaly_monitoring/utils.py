import pandas as pd
import tabulate


def quote_str(s: str):
    """ Returns a quoted string with '-quotes.
    """
    s = str(s)
    return f'\'{s}\''


def dataframe_to_str(df: pd.DataFrame) -> str:
    """ Returns a markdown table from a pandas DataFrame.
    """
    return tabulate.tabulate(df.values, headers=df.columns, tablefmt='simple')
