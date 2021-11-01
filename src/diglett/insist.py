"""Insist (assert) assumptions about data quality.

- These functions each verify a specific assumption.
- They are "non-breaking" by using HTML warnings instead of actual assertions.
- They each return the input object, allowing them to be used in DataFrame.pipe() chains.
"""

from typing import Any, Iterable, List, Union

from IPython.core.display import display, HTML
import pandas as pd


def _html_alert_danger(msg: str) -> HTML:
    """Display a message as a Bootstrap-styled HTML alert in a Jupyter notebook."""
    html_str = f'<div class="alert alert-danger" style="margin: 5px;">☠️ &nbsp; {msg}</div>'
    return HTML(html_str)


def _html_alert_success(msg: str) -> HTML:
    """Display a message as a Bootstrap-styled HTML alert in a Jupyter notebook."""
    html_str = f'<div class="alert alert-success" style="margin: 5px;">✅ &nbsp; {msg}</div>'
    return HTML(html_str)


def less_than_pct_null(
    df: pd.DataFrame,
    cols: Iterable[str] = None,
    pct: float = 0.01,
    return_alert: bool = False,
) -> Union[pd.DataFrame, HTML]:
    """Check that specified (or all) columns contain less than some % of null values."""
    if cols is None:
        sub_df = df
        cols = df.columns.tolist()
    else:
        sub_df = df[cols]

    cols_with_nulls = sub_df.isnull().any().loc[lambda x: x == True].index.tolist()

    if len(cols_with_nulls) / df.shape[0] > pct:
        alert = _html_alert_danger(
            f'More than {pct:.0%} null values in cols: {", ".join(cols_with_nulls)}'
        )
    else:
        alert = _html_alert_success(f'Less than {pct:.0%} null values in cols: {", ".join(cols)}')

    if return_alert:
        return alert
    else:
        display(alert)
        return df


def no_nulls(df: pd.DataFrame, cols: List[str] = None, **kwargs: Any) -> Union[pd.DataFrame, HTML]:
    """Check that specified (or all) columns do not contain null values."""

    return less_than_pct_null(df, cols, pct=0, **kwargs)


def more_than_pct_unique(
    df: pd.DataFrame,
    col: str,
    pct: Union[int, float] = 0.99,
    return_alert: bool = False,
) -> Union[pd.DataFrame, HTML]:
    """Check that a minimum pct. of values in a Series are unique."""

    srs = df[col]
    pct_unique = srs.nunique() / srs.shape[0]

    if pct_unique >= pct:
        alert = _html_alert_success(
            f'Cardinality: {pct_unique:.2%} of values in {srs.name} are unique. Threshold set is {pct:.2%}.'
        )
    else:
        alert = _html_alert_danger(
            f'Cardinality: {pct_unique:.2%} of values in {srs.name} are unique. Threshold set is {pct:.2%}.'
        )

    if return_alert:
        return alert
    else:
        display(alert)
        return df


def average_greater_than(
    df: pd.DataFrame,
    col: str,
    threshold: Union[int, float],
    return_alert: bool = False,
) -> Union[pd.DataFrame, HTML]:
    """Check that average of specified column is greater than some value."""

    avg = df[col].mean()

    if avg < threshold:
        alert = _html_alert_danger(
            f'Avg value of {col} is {avg:.2%}. Threshold is {threshold:.2%}.'
        )
    else:
        alert = _html_alert_success(
            f'Avg value of {col} is {avg:.2%}. Threshold is {threshold:.2%}.'
        )

    if return_alert:
        return alert
    else:
        display(alert)
        return df
