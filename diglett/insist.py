"""Insist (assert) assumptions about data quality

- These functions each verify a specific assumption.
- They are "non-breaking" by using HTML warnings instead of actual assertions.
- They each return the input object, allowing them to be used in DataFrame.pipe() chains.
"""

import pandas as pd
from IPython.core.display import HTML, display


def html_alert_danger(msg: str) -> None:
    """ Display a message as a Bootstrap-styled HTML alert in a Jupyter notebook """
    html_str = f'<div class="alert alert-danger" style="margin: 5px;">☠️ &nbsp; {msg}</div>'
    display(HTML(html_str))


def html_alert_success(msg: str) -> None:
    """ Display a message as a Bootstrap-styled HTML alert in a Jupyter notebook """
    html_str = f'<div class="alert alert-success" style="margin: 5px;">✅ &nbsp; {msg}</div>'
    display(HTML(html_str))


def no_duplicates(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """ Check that specified (or all) columns do not contain duplicates. """
    for col in cols:
        dupes = df[col].value_counts().loc[lambda x: x > 1]
        if len(dupes) == 0:
            html_alert_success(f'No duplicates in: {col}')
        else:
            html_alert_danger(f'Duplicates exist for: {col}')

    return df


def no_nulls(df: pd.DataFrame, cols: list=None) -> pd.DataFrame:
    """ Check that specified (or all) columns do not contain null values.  """
    if cols:
        sub_df = df[cols]
    else:
        sub_df = df
        col = ['<ALL>']

    cols_with_nulls = sub_df.isnull().any().loc[lambda x: x == True].index.tolist()

    if len(cols_with_nulls) > 0 :
        html_alert_danger(f'Null values in cols: {", ".join(cols_with_nulls)}')
    else:
        html_alert_success(f'No null values in cols: {", ".join(cols)}')

    return df


def less_than_pct_null(df: pd.DataFrame, cols: list=None, pct=0.01) -> pd.DataFrame:
    """ Check that specified (or all) columns contain less than some % of null values.  """
    if cols:
        sub_df = df[cols]
    else:
        sub_df = df
        col = ['<ALL>']

    cols_with_nulls = sub_df.isnull().any().loc[lambda x: x == True].index.tolist()

    if len(cols_with_nulls) / df.shape[0] > pct :
        html_alert_danger(f'More than {pct:.0%} null values in cols: {", ".join(cols_with_nulls)}')
    else:
        html_alert_success(f'Less than {pct:.0%} null values in cols: {", ".join(cols)}')

    return df


def more_than_pct_unique(df: pd.DataFrame, col: str, pct=0.99) -> pd.DataFrame:
    """ Check that a minimum pct. of values in a Series are unique. """

    srs = df[col]
    pct_unique = srs.nunique() / srs.shape[0]

    if pct_unique >= pct:
        html_alert_success(f'Cardinality: {pct_unique:.2%} of values in {srs.name} are unique. Threshold set is {pct:.2%}.')
    else:
        html_alert_danger(f'Cardinality: {pct_unique:.2%} of values in {srs.name} are unique. Threshold set is {pct:.2%}.')

    return df


def more_than_pct_avg(df: pd.DataFrame, col: str, pct=0.99) -> pd.DataFrame:
    """ Check that average of specified column is greater than some value.  """

    avg = df[col].mean()

    if avg < pct :
        html_alert_danger(f'Avg value of {col} is {avg:.2%}. Threshold is {pct:.2%}.')
    else:
        html_alert_success(f'Avg value of {col} is {avg:.2%}. Threshold is {pct:.2%}.')

    return df