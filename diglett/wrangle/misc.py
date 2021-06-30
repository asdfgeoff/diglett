import numpy as np
import pandas as pd
from ..utils import print_header_with_lines
from ..decorators import annotate_output


def reindex_by_sum(df, axis=1):
    """Reindex axis of a DataFrame according to it's sum."""
    row_order = df.sum(axis=1 - axis).sort_values(ascending=False).index.tolist()
    return df.reindex(row_order, axis=axis)


def fillnas(input_df, subset=None, value=0):
    """ """
    output_df = input_df.copy()
    for col in subset:
        output_df[col] = input_df[col].fillna(value)
    return output_df


def drop_nulls(input_df, subset=None):
    print_header_with_lines('DROPPING ROWS WITH NULLS')
    output_df = input_df.dropna(subset=subset)
    num_dropped = input_df.shape[0] - output_df.shape[0]
    pct_dropped = num_dropped / input_df.shape[0]
    if subset:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain null value in columns: {subset}')
    else:
        print(f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain null value in any column.')
    return output_df


def drop_infinite(input_df, subset=None):
    output_df = input_df.replace([np.inf, -np.inf], np.nan).dropna(subset=None)
    num_dropped = input_df.shape[0] - output_df.shape[0]
    pct_dropped = num_dropped / input_df.shape[0]
    if subset:
        print(
            f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain infinite value_col in columns: {subset}'
        )
        raise NotImplementedError
    else:
        print(
            f'Dropping {num_dropped} rows ({pct_dropped:.1%} of input) which contain infinite value_col in any column.'
        )
    return output_df


def categorical_fillna(df):
    """Hard-codes null values as strings, necessary for CatBoost."""
    null_cols = set((df.isnull().sum() > 1).loc[lambda x: x == True].index)
    cat_cols = set((df.dtypes == 'category').loc[lambda x: x == True].index)

    output_df = df.copy()
    for col in null_cols & cat_cols:
        output_df[col] = output_df[col].cat.add_categories(['NULL']).fillna('NULL')

    return output_df


def bucket_long_tail_categories(input_df: pd.DataFrame, other_after=100):
    """Automatically split any categorical columns into boolean columns for each value.

    Args:
        input_df (pd.DataFrame): The entire DataFrame to operate on.
        other_after (int): The index after which to bucket long-tail values into 'other'

    Returns:
        pd.DataFrame: Output dataframe
    """

    print_header_with_lines('BUCKET LONG-TAIL VALUES')
    output_df = input_df.copy()
    category_cols = input_df.select_dtypes(include=['category']).columns

    for col in category_cols:
        if input_df[col].nunique() > other_after:
            most_common_values = input_df[col].value_counts().nlargest(other_after)

            output_df[col] = (
                input_df[col]
                .astype('object')
                .where((input_df[col].isin(most_common_values.index)) | (input_df[col].isnull()), other='Other')
                .astype('category')
            )

            print(f"{col}: Replaced {(output_df[col] == 'Other').sum()} values with 'Other'")

    return output_df


if __name__ == '__main__':
    pass
