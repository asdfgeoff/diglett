"""Tools related to df.groupby()."""

from functools import singledispatch
from typing import Union

import pandas as pd


@singledispatch
def group_other(
    data: Union[pd.Series, pd.DataFrame],
    n: int = 10,
    other_val: str = '…',
    sort_by: str = None,
):
    """Group the "long-tail" dimensions (beyond top N) of a DataFrame or Series together.

    Assumptions:

    * Index does not matter
    * All non-numeric columns are dimensions
    * If multiple numeric columns, sort by right-most before grouping

    Args:
        data: A series or dataframe as input.
        n: Values beyond this point get grouped as "other".
        other_val: The string with which to represent "other" values.
        sort_by: The column by which to sort the dataframe, before grouping.

    """
    raise NotImplementedError


@group_other.register
def _group_other_df(
    df: pd.DataFrame, n: int = 10, other_val: str = '…', sort_by: str = None
) -> pd.DataFrame:
    """Implement group_other() for DataFrame input."""

    # infer which columns to group by and aggregate
    num_cols = df.select_dtypes('number').columns.tolist()
    cat_cols = df.select_dtypes(exclude='number').columns.tolist()

    if not sort_by:
        sort_by = num_cols[-1]
    df = df.sort_values(by=sort_by, ascending=False)

    # replace long-tail with "other" placeholder
    df.iloc[n:, df.columns.get_indexer(cat_cols)] = other_val

    return df.groupby(cat_cols).sum().sort_values(by=sort_by, ascending=False).reset_index()


@group_other.register
def _group_other_srs(srs: pd.Series, n: int = 10, other_val: str = '…') -> pd.Series:
    """Implement group_other() for a Series input."""

    assert srs.dtype.kind == 'i', 'Expecting an int'

    srs = srs.sort_values(ascending=False)
    idx = srs.index.to_series()
    idx[n:] = other_val
    srs.index = idx

    return srs.groupby(level=0).sum().sort_values(ascending=False)


if __name__ == '__main__':
    pass  # pragma: no cover
