"""Tools for transforming input data into more usable form."""

from typing import Any, List, Optional, Union

import numpy as np
import pandas as pd


def reindex_by_sum(df: pd.DataFrame, axis: int = 1, margin_col: str = None) -> pd.DataFrame:
    """Reindex axis of a DataFrame according to it's sum.

    Args:
        df: The DataFrame to reindex.
        axis: The axis upon which to reindex.
        margin_col: This column/index value will be excluded from the sort (end).
    """

    row_order = df.sum(axis=1 - axis).sort_values(ascending=False).index.tolist()

    if margin_col:
        row_order.remove('All')
        row_order.extend(['All'])

    return df.reindex(row_order, axis=axis)


def fillnas(
    input_df: pd.DataFrame,
    subset: Optional[List[str]] = None,
    value: Any = 0,
) -> pd.DataFrame:
    """Apply fillna to a subset of columns.

    Roughly equivalent to df[subset] = df[subset].fillna(value)

    Args:
        input_df: The DataFrame to operate on.
        subset: A list of the columns to operate on.
        value: The value with which to fill nulls.
    """

    output_df = input_df.copy()
    if subset is None:
        subset = output_df.columns.tolist()
    for col in subset:
        output_df[col] = input_df[col].fillna(value)
    return output_df


def winsorize(
    srs: pd.Series,
    lower: Union[int, float] = 0,
    upper: Union[int, float] = 0.99,
    verbose: bool = True,
) -> pd.Series:
    """Winsorize a series at specified quantiles.

    Args:
        srs: The pandas Series to be winsorized.
        lower: Values below this point get winsorized.
        upper: Values above this point get winsorized.
        verbose: Whether to print info to stdout for debugging.

    """

    lower_val, upper_val = srs.quantile([lower, upper]).tolist()
    trimmed = srs.clip(lower=lower_val, upper=upper_val)

    if verbose:
        print(f'Winsorizing {srs.name} to range: [{lower_val:.2f}, {upper_val:.2f}]')
        print(f'Previous mean:\t {srs.mean():.2f}')
        print(f'New mean:\t {trimmed.mean():.2f}', '\n')

    return trimmed


def multi_moving_average(
    df: pd.DataFrame,
    window: int = 7,
    min_periods: int = 1,
) -> pd.DataFrame:
    """Apply a moving average to a DataFrame with a 2-level index, where the second is a dimension.

    Args:
        df: The DataFrame to operate on.
        window: Passed directly as argument to df.rolling()
        min_periods: Passed directly as argument to df.rolling()

    """

    assert (
        df.select_dtypes(include=np.number).columns.tolist() == df.columns.tolist()
    ), 'Expecting all columns to be numeric'
    assert df.index.nlevels == 2, 'Expecting two levels of index'
    assert (
        df.index.get_level_values(1).dtype == 'object'
    ), 'Expecting second level of index to be a string (dim)'

    return (
        df.sort_index()
        .groupby(level=1)
        .transform(lambda x: x.rolling(window=window, min_periods=min_periods).mean())
    )


if __name__ == '__main__':
    pass  # pragma: no cover
