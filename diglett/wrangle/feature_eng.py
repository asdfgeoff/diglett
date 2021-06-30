import numpy as np
import pandas as pd

from ..utils import print_header_with_lines
from .misc import categorical_fillna


def one_hot_encode_categoricals(input_df: pd.DataFrame):
    """Automatically split any categorical columns into boolean columns for each value.

    Args:
        input_df (pd.DataFrame): The entire DataFrame to operate on.
        other_after (int): The index after which to bucket long-tail values into 'other'

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


def compare_to_prev(df: pd.DataFrame, prev_cols: list) -> pd.DataFrame:
    """Assigns a float bool column to DataFrame reflecting whether a value equals another value.

    Value is NaN when previous value does not exist.

    """
    print_header_with_lines('Generate comparison features')
    output_df = df.copy()
    new_col = 'is_same_as_prev_{}'

    compare_pairs = [(col, col.replace('prev_', '')) for col in prev_cols]
    print([new_col.format(tupl[0]) for tupl in compare_pairs])

    for prev_col, col in compare_pairs:
        output_df[new_col.format(col)] = (output_df[col] == output_df[prev_col]).where(
            output_df[prev_col].isnull() == False
        )

    return output_df


def make_comparison_bools(df: pd.DataFrame, comparisons: dict) -> pd.DataFrame:
    """Assigns a float bool column to DataFrame reflecting whether a value equals another value.

    Value is NaN when previous value does not exist.

    Args:
        comparisons (dict): Tuples of column names to compare, e.g.: output_column_name: (col_a, col_b)

    """
    print_header_with_lines('Generate comparison features')
    output_df = df.copy()

    for output_col_name, cols in comparisons.items():
        col_a, col_b = cols
        print(f'{output_col_name}:\t{col_a} ↔ {col_b}')

        try:
            comparison_srs = df[col_a] == df[col_b]
        except TypeError:
            comparison_srs = df[col_a].astype('object') == df[col_b].astype('object')

        with_nans = comparison_srs.where((df[col_a].isnull() == False) & (df[col_b].isnull() == False))
        output_df[output_col_name] = with_nans

    return output_df


from sklearn.preprocessing import OrdinalEncoder


def ordinal_encode_categoricals(X_train, X_test):
    """Fit an sklearn OrdinalEncoder on a combined test/train dataset and return transforms on each individual dataset."""

    X_train_out, X_test_out = X_train.copy(), X_test.copy()

    X_all = pd.concat([X_train, X_test]).pipe(categorical_fillna)
    cat_cols = X_all.select_dtypes('category').dtypes.index.values.tolist()
    enc = OrdinalEncoder()
    enc.fit(X_all[cat_cols])

    X_train_out[cat_cols] = enc.transform(X_train[cat_cols].pipe(categorical_fillna))
    X_test_out[cat_cols] = enc.transform(X_test[cat_cols].pipe(categorical_fillna))

    return X_train_out, X_test_out


def sanitize_for_logistic_regression(df):
    disallowed_dtypes = ['datetime', 'object']
    for dtype in disallowed_dtypes:
        disallowed_columns = df.select_dtypes(dtype).columns
        assert len(disallowed_columns) == 0, f'Columns of dtype {dtype}: {", ".join(disallowed_columns)}'

    assert df.isnull().any().any() == False, 'No null values are allowed'


def make_col_x_conditional_on_y(df: pd.DataFrame, cols: str, condition_on: str):
    """If a row does not match condition_on, replace its values in cols with zero."""
    df = df.copy()

    # wrangle single arguments into lists
    for arg in [cols, condition_on]:
        if isinstance(arg, str):
            arg = [arg]
        elif not isinstance(arg, list):
            raise ValueError

    # verify that column being conditioned is a float, not a bool
    if isinstance(cols, str):
        assert df[cols].dtype == np.float, 'Boolean must be encoded as a float to allow for nulls'
    elif isinstance(cols, list):
        assert (df[cols].dtypes == np.float).all(), 'Boolean must be encoded as a float to allow for nulls'

    cond_bool = df[condition_on].fillna(0).astype(bool)
    df.loc[cond_bool, cols] = df.loc[cond_bool, cols].fillna(0)
    df.loc[~cond_bool, cols] = np.nan
    return df


def assign_binned_column(df: pd.DataFrame, col: str, bins: list, labels=None, output_col=None) -> pd.DataFrame:
    """Wrapper for pd.cut with custom bins, and optional labels."""
    if not output_col:
        output_col = col + '_binned'

    if not labels:
        labels = [f'{x}-{y-1}' for x, y in zip(bins[:-1], bins[1:])]

    df = df.copy()
    df[output_col] = pd.cut(df[col], bins=bins, labels=labels).astype(str)

    return df


if __name__ == '__main__':
    pass
