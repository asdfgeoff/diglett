"""Functions which produce some sort of output from a DataFrame."""

from typing import List, Optional, Union

from IPython.core.display import display, display_html
import pandas as pd
from pandas.io.formats.style import Styler


def format_helper(
    df: Union[pd.DataFrame, Styler],
    int_cols: Optional[List[str]] = None,
    pct_cols: Optional[List[str]] = None,
    delta_cols: Optional[List[str]] = None,
    monospace: bool = True,
    hide_index: bool = True,
    return_output: bool = False,
) -> Optional[Styler]:
    """Apply common formatting using pandas.DataFrame.style methods.

    Args:
        df: The pandas DataFrame to be displayed.
        int_cols: Optional hard-coded list of columns to display as integers.
        pct_cols: Optional hard-coded list of columns to display as percentages.
        delta_cols: Optional hard-coded list of columns to display as "deltas".
        monospace: Whether to display with monospace font.
        hide_index: Whether to hide the index of the DataFrame.
        return_output: This is only used for testing purposes.

    """

    if isinstance(df, pd.core.frame.DataFrame):
        output = df.style
    elif isinstance(df, Styler):
        output = df
    else:
        raise ValueError

    formats = {'int_cols': '{:.0f}', 'pct_cols': '{:.2%}', 'delta_cols': '{:+.2%}'}

    if int_cols is None:
        int_cols = [c for c in df.columns if (str.startswith(c, 'n_') or str.startswith(c, 'num_'))]

    if pct_cols is None:
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

    if return_output:
        return output
    else:
        display(output)
        return None


def display_side_by_side(*args: pd.DataFrame) -> None:  # pragma: no cover
    """Output an array of pandas DataFrames side-by-side in a Jupyter notebook to conserve vertical space."""
    html_str = ''
    for df in args:
        html_str += df.to_html()
    display_html(html_str.replace('table', 'table style="display:inline"'), raw=True)


if __name__ == '__main__':
    pass  # pragma: no cover
