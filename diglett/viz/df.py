import pandas as pd
from IPython.core.display import display
from warnings import warn

from ..utils import h3, h7


def format_helper(
    df: pd.DataFrame,
    int_cols=None,
    pct_cols=None,
    delta_cols=None,
    monospace=True,
    hide_index=True,
) -> None:
    """Apply common formatting using pandas.DataFrame.style methods"""

    if isinstance(df, pd.core.frame.DataFrame):
        output = df.style
    elif isinstance(df, pd.io.formats.style.Styler):
        output = df
    else:
        raise ValueError

    formats = {'int_cols': '{:.0f}', 'pct_cols': '{:.2%}', 'delta_cols': '{:+.2%}'}

    if not int_cols:
        int_cols = [c for c in df.columns if (str.startswith(c, 'n_') or str.startswith(c, 'num_'))]

    if not pct_cols:
        pct_cols = [c for c in df.columns if (str.startswith(c, 'p_') or str.startswith(c, 'pct_'))]

    output = output.format({col: formats['int_cols'] for col in int_cols}).format(
        {col: formats['pct_cols'] for col in pct_cols}
    )

    if delta_cols:
        delta_cols = output.format({col: formats['delta_cols'] for col in delta_cols})

    if monospace:
        output = output.set_properties(**{'font-family': 'Menlo'})

    if hide_index:
        output = output.hide_index()

    display(output)


def display_insight(df: pd.DataFrame, title='', subtitle='', assertion=None) -> None:
    """Display a pandas DataFrame as a presentable display_insight.

    Args:
        df (pd.DataFrame): The table to be displayed
        fmt (str): String representation of formatting to apply to dataframe output (e.g. {:.0%} for percentages )
        title (str): The key takeaway or display_insight from the table
        subtitle (str): A more objective description of the table contents
        assertion (func): A lambda statement to check the validity of the display_insight against the contents of the dataframe

    """

    from textwrap import wrap

    if title:
        h3(title)
    if subtitle:
        split = '<br>'.join(wrap(subtitle, width=60))
        h7(split)

    else:
        display(df)

    if assertion:
        if not assertion(df):
            warn('This insight may no longer be true!')


if __name__ == '__main__':
    pass
