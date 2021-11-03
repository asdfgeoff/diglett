"""Tools for exploratory data analysis (EDA).

These help understand the nature of some data, mostly by displaying stuff, not returning anything.
"""

from functools import singledispatch
from typing import Optional, Union

from IPython.core.display import display
import numpy as np
import pandas as pd

from .group import group_other
from .output import format_helper
from .transform import reindex_by_sum


@singledispatch
def show_top_n(
    data: Union[pd.Series, pd.DataFrame],
    n: int = 10,
    show_output: bool = True,
    other_val: str = '…',
) -> Optional[Union[pd.Series, pd.DataFrame]]:
    """Cleanly display the top N values from a "group by count" SQL output.

    Args:
        data: A series or dataframe, with columns (<dim>, num_).
        n: The number of rows to show, before grouping remainder as "other".
        show_output: If true, display result "nicely", else return the actual df.
        other_val: The value to which values beyond the top N are grouped.

    """
    raise NotImplementedError


@show_top_n.register
def _show_top_n_df(
    df: pd.DataFrame,
    n: int = 10,
    show_output: bool = True,
    other_val: str = '…',
) -> Optional[pd.DataFrame]:
    """Implement show_top_n() for DataFrame input."""

    df = df.copy()
    df.iloc[:, :-1] = df.iloc[:, :-1].astype(str).fillna('< NULL >')

    df = df.pipe(group_other, n=n, other_val=other_val).pipe(lambda x: x.set_index(x.columns[0]))

    # Force OTHER category to appear at the bottom
    if other_val in df.index:
        df = pd.concat([df.drop(other_val), df.loc[[other_val], :]])

    num_col = df.columns[-1]
    df = df.assign(pct_=lambda x: x[num_col] / x[num_col].sum()).reset_index()

    if show_output:
        format_helper(df)
        return None
    else:
        return df


@show_top_n.register
def _show_top_n_srs(
    srs: pd.Series,
    n: int = 10,
    show_output: bool = True,
    other_val: str = '…',
) -> Optional[pd.Series]:
    """Implement show_top_n() for Series input."""

    srs = srs.copy()
    srs.index = srs.index.astype(str).fillna('< NULL >')

    srs = srs.pipe(group_other, n=n, other_val=other_val)

    # Force OTHER category to appear at the bottom
    if other_val in srs.index:
        srs = srs.drop(other_val).append(srs.loc[[other_val]])

    srs = srs.pipe(pd.DataFrame).assign(pct_=lambda x: x / x.sum()).reset_index()

    if show_output:
        format_helper(srs)
        return None
    else:
        return srs


def tabulate(
    df: pd.DataFrame,
    normalize: bool = False,
    sorted: bool = True,
    return_output: bool = False,
) -> Optional[pd.DataFrame]:
    """Pivot a DataFrame to show a numeric column across each of two dimensions.

    Args:
        df: DataFrame w/ columns: (dim_A, dim_B, num_).
        normalize: Whether to return absolute counts (default) or normalize by total.
        sorted: Whether to sort index (and columns) to have highest row (or column) sums first.
        return_output: By default, output is displayed, but can also be returned.

    """

    # sanity check on inputs
    assert len(df.columns) == 3, 'Expecting exactly three columns'
    dim_A, dim_B, num_col = df.columns

    pivot = pd.crosstab(
        index=df[dim_A],
        columns=df[dim_B],
        values=df[num_col],
        aggfunc=sum,
        margins=True,
        normalize=normalize,
    ).fillna(0)

    # fmt: off
    if sorted:
        pivot = (
            pivot
            .pipe(reindex_by_sum, axis=0, margin_col='All')
            .pipe(reindex_by_sum, axis=1, margin_col='All')
        )
    # fmt on

    if normalize:
        format_str: Optional[str] = '{:.0%}'
    else:
        format_str = None

    if return_output:
        return pivot
    else:
        display(pivot.style.set_properties(**{'font-family': 'Menlo'}).format(format_str))
        return None


def summarize(df: pd.DataFrame, return_output: bool = False) -> Optional[pd.DataFrame]:
    """Show a better summary than df.info().

    Incl. number of rows, memory, nulls, unique, (min/mean/max) of numerics, mode of string cols.
    """

    df = df.copy()
    n_rows = df.shape[0]

    # convert object dtypes to strings, to avoid error on df.nunique() called on lists
    obj_cols = df.dtypes.loc[lambda x: x == 'object'].index.tolist()
    df.loc[:, obj_cols] = df.loc[:, obj_cols].astype(str)

    # assemble the "main" summary, which applies to all columns
    info_df = pd.concat(
        [
            df.dtypes.rename('dtype'),
            df.isnull().sum().rename('Null (#)'),
            df.nunique().rename('Unique (#)'),
        ],
        axis=1,
    )
    info_df[['Null (%)', 'Unique (%)']] = info_df[['Null (#)', 'Unique (#)']] / n_rows
    info_df = info_df.reindex(['dtype', 'Null (#)', 'Null (%)', 'Unique (#)', 'Unique (%)'], axis=1)

    # add mode (most common value) for object (string) columns
    object_cols = df.select_dtypes(include='object').columns.tolist()
    info_df.loc[object_cols, 'mode'] = df[object_cols].mode().iloc[0]

    # add min/mean/max for numeric columns
    # reindex step is for pandas=1.0.4, which otherwise throws a key error
    # see: https://stackoverflow.com/questions/30926670/add-multiple-empty-columns-to-pandas-dataframe
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    info_df = info_df.reindex(list(info_df.columns) + ['min', 'mean', 'max'], axis=1)
    info_df.loc[num_cols, ['min', 'mean', 'max']] = df[num_cols].agg(['min', 'mean', 'max']).T

    # Workaround for style.format(precision=…) only supported on pandas≥1.3.0
    pd.set_option('precision', 2)
    output = (
        info_df.style.set_properties(**{'font-family': 'Menlo'})
        .format({'Null (%)': '{:.2%}', 'Unique (%)': '{:.2%}'}, na_rep='')
        .background_gradient(cmap='Reds', vmin=0, vmax=1, subset=['Null (%)'])
    )

    display(output)

    mem_gb = df.memory_usage(deep=True).sum() / 10 ** 9
    print(f'Number of rows: {n_rows}\tMemory: {mem_gb:.2f} GB')

    if return_output:
        return info_df
    else:
        return None


if __name__ == '__main__':
    pass  # pragma: no cover
