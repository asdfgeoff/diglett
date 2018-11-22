import pandas as pd
from IPython.core.display import HTML, display
from IPython.display import display_html
import numpy as np


def h4(input_str):
    display(HTML(f'<h4>{input_str}</h4>'))


def display_side_by_side(*args):
    html_str = ''
    for df in args:
        html_str += df.to_html()
    display_html(html_str.replace('table', 'table style="display:inline"'), raw=True)


def infer_dtypes(input_df: pd.DataFrame, categorical_threshold=0.01) -> pd.DataFrame:
    """ Attempt to coerce dtypes to be numerical, datetime, or categorical rather than object.
    Args:
        input_df (pd.DataFrame): The DataFrame object whose dtypes are being inferred.
        categorical_threshold (float): The level of normalized cardinality below which to consider a field catagorical.
    """
    output_df = input_df.copy()
    assert input_df.columns.value_counts().max() == 1, 'Non-unique column names'
    for c in input_df.select_dtypes('object').columns:

        try:
            output_df[c] = pd.to_numeric(input_df[c])
            continue
        except (ValueError, TypeError):
            pass
        try:
            output_df[c] = pd.to_datetime(input_df[c])
            continue
        except (ValueError, TypeError):
            pass

        if input_df[c].nunique() / input_df[c].notnull().count() < categorical_threshold:
            output_df[c] = input_df[c].astype('category')
            continue

    return output_df


def describe_dtypes(input_df, top_n_cats=10):
    """ A more comprehensive overview of your data, inspired by pd.DataFrame.describe()

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
            h4(dtype_name)

            try:
                sub_df = input_df.select_dtypes(include=dtype_cls)
                nulls_summary = sub_df.isnull().agg(['sum', 'mean']).T.rename(columns={'sum': 'num_null', 'mean': 'pct_null'})
                if dtype_name == 'Categoricals':
                    dfs = [sub_df[col].value_counts(dropna=False, normalize=True).head(top_n_cats).pipe(pd.DataFrame) for col in sorted(sub_df.keys())]
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
