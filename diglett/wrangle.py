""" Functions for wrangling a dataset into a tidy format with correct dtypes.

Examples:
    You can infer dtypes for imported data, then apply a bunch of transformations, and finally describe them::

        df = (pd
              .read_csv('data.csv')
              .pipe(infer_dtypes, categorical_threshold=0.10)
              .pipe(fillnas, subset=['category', 'type'])
              .pipe(drop_nulls, subset=['id', 'ts'])
              .pipe(drop_infinite)
              .pipe(bucket_long_tail_categories)
              .pipe(one_hot_encode_categoricals)

        describe_dtypes(df)

"""
from typing import Tuple
import numpy as np
import pandas as pd
from IPython.core.display import display
import humanfriendly
from .display import header, display_side_by_side, print_header_with_lines


def infer_dtypes(input_df: pd.DataFrame, categorical_threshold: float = 0.01) -> pd.DataFrame:
    """ Attempt to coerce dtypes to be numerical, datetime, or categorical rather than object.

    Args:
        input_df: The DataFrame object whose dtypes are being inferred.
        categorical_threshold: The level of normalized cardinality below which to consider a field catagorical.

    Returns:
        DataFrame of same dimensions as input, but with modified column dtypes.

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


def describe_dtypes(input_df: pd.DataFrame, top_n_cats: int = 10, return_df: bool = False) -> pd.DataFrame:
    """ A more comprehensive overview of your data, inspired by pd.DataFrame.describe()

    Splits output by dtype to provide a more relevant summary of each, including number and pct of null values.

    Args:
        input_df: The dataframe to be desribed.
        top_n_cats: The number of most frequent values to include in summary of categorical columns.
        return_df: Whether or not to return the input DataFrame, such that function can be used in a .pipe() chain.

    """

    mem_bytes = input_df.memory_usage(deep=True).sum()
    print(f'Number of rows: {input_df.shape[0]}')
    print(f'Size in memory: {humanfriendly.format_size(mem_bytes)}')

    with pd.option_context('float_format', lambda x: '%.3f' % x, 'display.max_rows', 200):

        dtype_map = [
            ('Numerics', np.number),
            ('Categoricals', 'category'),
            ('Booleans', bool),
            ('Datetimes', 'datetime'),
            ('Object (strings)', 'object'),
        ]

        for dtype_name, dtype_cls in dtype_map:
            header(dtype_name, size=3)

            try:
                sub_df = input_df.copy().select_dtypes(include=dtype_cls)
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

    if return_df:
        return input_df


def fillnas(input_df: pd.DataFrame, subset: list = None, fill_value=0, verbose: bool = True) -> pd.DataFrame:
    """ Fills nulls in selected columns from a DataFrame then returns input in a DataFrame.pipe() compatible way. """
    output_df = input_df.copy()

    if verbose:
        print_header_with_lines(f'FILLING NULL VALUES IN COLUMNS: {subset}')

    for col in subset:
        if verbose:
            num_nulls = input_df[col].isnull().sum()
            pct_nulls = input_df[col].isnull().mean()
            print(f'Pre-transform null values: {num_nulls} ({pct_nulls:.2%} of rows)')
        output_df[col] = input_df[col].fillna(fill_value)
    return output_df


def drop_nulls(input_df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """ Drops nulls in selected columns from a DataFrame then returns input in a DataFrame.pipe() compatible way. """
    print_header_with_lines('DROPPING ROWS WITH NULLS')
    output_df = input_df.dropna(subset=subset)
    num_dropped = input_df.shape[0] - output_df.shape[0]
    pct_dropped = num_dropped / input_df.shape[0]
    if subset:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain null value in columns: {subset}')
    else:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain null value in any column.')
    return output_df


def drop_infinite(input_df: pd.DataFrame, subset: list = None) -> pd.DataFrame:
    """ Drops infinite values in selected columns then returns df in a DataFrame.pipe() compatible way. """

    output_df = input_df.replace([np.inf, -np.inf], np.nan).dropna(subset=None)
    num_dropped = input_df.shape[0] - output_df.shape[0]
    pct_dropped = num_dropped / input_df.shape[0]
    if subset:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain infinite value_col in columns: {subset}')
        raise NotImplementedError
    else:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain infinite value_col in any column.')
    return output_df


def categorical_fillna(df: pd.DataFrame) -> pd.DataFrame:
    """ Hard-codes null values as strings, necessary for CatBoost. """
    null_cols = set((df.isnull().sum() > 1).loc[lambda x: x == True].index)
    cat_cols = set((df.dtypes == 'category').loc[lambda x: x == True].index)

    output_df = df.copy()
    for col in (null_cols & cat_cols):
        output_df[col] = output_df[col].cat.add_categories(['NULL']).fillna('NULL')

    return output_df


def bucket_long_tail_categories(input_df: pd.DataFrame, other_after: int = 100) -> pd.DataFrame:
    """ Replace long-tail values in each column with 'Other' to reduce cardinality.

    Args:
        input_df: The entire DataFrame to operate on.
        other_after: The index after which to bucket long-tail values into 'other'

    """

    print_header_with_lines('BUCKET LONG-TAIL VALUES')
    output_df = input_df.copy()
    category_cols = input_df.select_dtypes(include=['category']).columns

    for col in category_cols:
        if input_df[col].nunique() > other_after:
            most_common_values = input_df[col].value_counts().nlargest(other_after)

            output_df[col] = (input_df[col]
                              .astype('object')
                              .where((input_df[col].isin(most_common_values.index)) | (input_df[col].isnull()), other='Other')
                              .astype('category'))

            print(f"{col}: Replaced {(output_df[col] == 'Other').sum()} values with 'Other'")

    return output_df


def one_hot_encode_categoricals(input_df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    """Automatically split any categorical columns into boolean columns for each value.

    Args:
        input_df: The entire DataFrame to operate on.

    Returns:
        pd.DataFrame: Output dataframe
        dict: Categorical mappings (useful for inverse transform during feature importance measurement)
    """

    print_header_with_lines('ONE-HOT ENCODE CATEGORICALS')
    category_cols = input_df.select_dtypes(include=['category']).columns
    to_concat = []
    categorical_mappings = {}

    for col in category_cols:

        clean_col = input_df[col].cat.remove_unused_categories().str.lower().replace(',', '').replace(' ', '_')
        dummies = pd.get_dummies(clean_col, prefix='is_{}'.format(col))
        to_concat.append(dummies)
        categorical_mappings[col] = list(dummies.columns)

    print(f'Converted {len(category_cols)} categorical columns to {sum([x.shape[1] for x in to_concat])} columns.')
    return pd.concat([input_df.drop(category_cols, axis=1)] + to_concat, axis=1), categorical_mappings


def cast_bools_to_float(df: pd.DataFrame) -> pd.DataFrame:
    """ Hard-codes booleans as floats, necessary for CatBoost. """
    bool_cols = set((df.dtypes == bool).loc[lambda x: x == True].index)
    output_df = df.copy()
    for col in bool_cols:
        output_df[col] = output_df[col].astype(float)

    return output_df


def attr(srs: pd.Series):
    """ Returns a record-level result as an aggregation.

    IF there are multiple values of the rec-rdlevel field then it will return '*' instead.
    Based on Tableau's ATTR aggregation: https://community.tableau.com/docs/DOC-1355

    """
    if hasattr(srs, 'cat'):
        srs = srs.cat.as_ordered()

    min_val, max_val = srs.min(), srs.max()
    is_same = (min_val == max_val)

    return np.where(is_same, min_val, None)


def max_one(srs: pd.Series):
    raise NotImplementedError()


def order_categorical(srs: pd.Series, ordered_categories: list) -> pd.Series:
    """ Order a categorical column based on a manually-defined order of categories.

    After ordering, the property srs.cat.codes can be used directly as an ordinal encoding.

    """
    assert set(srs.unique()) == set(ordered_categories), 'Manual ordering does not match observed values'
    output = srs.copy()

    if not hasattr(srs, 'cat'):
        output = srs.astype('category')

    output = output.cat.set_categories(ordered_categories, ordered=True)
    assert output.cat.ordered
    return output


if __name__ == '__main__':
    pass
