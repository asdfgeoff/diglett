from textwrap import wrap
from warnings import warn
from functools import singledispatch
from typing import Union, Optional

import numpy as np
import pandas as pd

from IPython.display import display_html
from IPython.core.display import display

from .utils import h3
from .wrangle import group_other
from .viz import format_helper


@singledispatch
def show_top_n(
    data: Union[pd.Series, pd.DataFrame], n=10, show_output=True, other_val='…'
) -> Optional[Union[pd.Series, pd.DataFrame]]:
    """Cleanly display the top N values from a "group by count" SQL output.

    Args:
        data: with columns (<dim>, num_)
    """
    raise NotImplementedError


@show_top_n.register
def _show_top_n_df(df: pd.DataFrame, n=10, show_output=True, other_val='…') -> Optional[pd.DataFrame]:
    """ """

    df = df.copy()

    assert df.dtypes[-1].kind == 'i', 'Expecting final column to be an int'
    df.iloc[:, :-1] = df.iloc[:, :-1].astype(str).fillna('< NULL >')

    df = df.pipe(group_other, n=n, other_val=other_val).pipe(lambda x: x.set_index(x.columns[0]))

    # Force OTHER category to appear at the bottom
    if other_val in df.index:
        df = pd.concat([df.drop(other_val), df.loc[[other_val], :]])

    df = df.assign(pct_=lambda x: x['num_'] / x['num_'].sum()).reset_index()

    if show_output:
        format_helper(df)
    else:
        return df


@show_top_n.register
def _show_top_n_srs(srs: pd.Series, n=10, show_output=True, other_val='…') -> Optional[pd.Series]:
    """ """

    srs = srs.copy()

    assert srs.dtype.kind == 'i', 'Expecting values to be an int'
    srs.index = srs.index.astype(str).fillna('< NULL >')

    srs = srs.pipe(group_other, n=n, other_val=other_val)

    # Force OTHER category to appear at the bottom
    if other_val in srs.index:
        srs = srs.drop(other_val).append(srs.loc[[other_val]])

    srs = srs.pipe(pd.DataFrame).assign(pct_=lambda x: x / x.sum()).reset_index()

    if show_output:
        format_helper(srs)
    else:
        return srs


def pivot_2d(df: pd.DataFrame) -> None:
    """Pivot a DataFrame to show relative % across each of two dimensions.

    Args:
        df: a DataFrame w/ columns (dim_A, dim_B, num_)

    """

    pivot = (
        df.copy()
        .assign(num_=lambda x: x['num_'] / x['num_'].sum())
        .pivot_table(index=df.columns[0], columns=df.columns[1], aggfunc=sum, fill_value=0, margins=True)
        .droplevel(0, axis=1)
    )

    display(pivot.style.set_properties(**{'font-family': 'Menlo'}).format('{:.2%}'))


def display_side_by_side(*args):
    """Output an array of pandas DataFrames side-by-side in a Jupyter notebook to conserve vertical space."""
    html_str = ''
    for df in args:
        html_str += df.to_html()
    display_html(html_str.replace('table', 'table style="display:inline"'), raw=True)


def minimal_describe(df: pd.DataFrame) -> None:
    """Print the number of rows and list of columns in a DataFrame."""
    print(f'Rows: {df.shape[0]}')
    pretty_print_cols = '\n\t'.join(df.columns.tolist())
    print(f'Columns:\n\t{pretty_print_cols}')


def describe_dtypes(input_df, top_n_cats=10):
    """A more comprehensive overview of your data, inspired by pd.DataFrame.describe()

    Splits output by dtype to provide a more relevant summary of each, including number and pct of null values.

    Args:
        input_df (pd.DataFrame): The dataframe to be desribed.
        top_n_cats (int): The number of most frequent values to include in summary of categorical columns.

    """

    mem_gb = input_df.memory_usage(deep=True).sum() / 10 ** 9
    print(f'Number of rows: {input_df.shape[0]}')
    print(f'Size in memory: {mem_gb:.2f} GB')

    with pd.option_context('float_format', lambda x: '%.3f' % x, 'display.max_rows', 200):

        dtype_map = [
            ('Numerics', np.number),
            ('Categoricals', 'category'),
            ('Booleans', bool),
            ('Datetimes', 'datetime'),
            ('Object (strings)', 'object'),
        ]

        for dtype_name, dtype_cls in dtype_map:
            h3(dtype_name)

            try:
                sub_df = input_df.select_dtypes(include=dtype_cls)
                nulls_summary = (
                    sub_df.isnull().agg(['sum', 'mean']).T.rename(columns={'sum': 'num_null', 'mean': 'pct_null'})
                )
                if dtype_name == 'Categoricals':
                    dfs = [
                        sub_df[col].value_counts(dropna=False, normalize=True).head(top_n_cats).pipe(pd.DataFrame)
                        for col in sorted(sub_df.keys())
                    ]
                    display_side_by_side(*dfs)
                else:
                    if dtype_name == 'Booleans':
                        described_df = sub_df.mean().pipe(lambda x: pd.DataFrame({'mean': x})).sort_index()
                    else:
                        described_df = sub_df.describe().T.join(nulls_summary).sort_index()
                        described_df[['count', 'num_null']] = described_df[['count', 'num_null']].astype(int)
                    display(described_df)

            except ValueError:
                print(f'No {dtype_name} columns found.')


def better_info(df: pd.DataFrame):
    """Show a better summary than df.info()"""

    df = df.copy()

    n_rows = df.shape[0]
    print(f'Number of rows: {n_rows}')

    mem_gb = df.memory_usage(deep=True).sum() / 10 ** 9
    print(f'Size in memory: {mem_gb:.2f} GB')

    # convert object dtypes to strings, to avoid error on df.nunique() called on lists
    obj_cols = df.dtypes.loc[lambda x: x == 'object'].index.tolist()
    df.loc[:, obj_cols] = df.loc[:, obj_cols].astype(str)

    info_df = pd.concat(
        [df.dtypes.rename('dtype'), df.isnull().sum().rename('num_null'), df.nunique().rename('num_unique')], axis=1
    ).assign(pct_null=lambda x: x['num_null'] / n_rows, pct_unique=lambda x: x['num_unique'] / n_rows)

    output = (
        info_df.style.set_properties(**{'font-family': 'Menlo'})
        .format({'pct_null': '{:.2%}', 'pct_unique': '{:.2%}'})
        .background_gradient(cmap='Reds', vmin=0, vmax=1, subset=['pct_null'])
    )

    display(output)


def max_abs_of_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Get the maximum absolute value from a DataFrame with multiple columns."""
    min_val = df.min().min()
    max_val = df.max().max()
    return max(abs(min_val), abs(max_val))


if __name__ == '__main__':
    pass
