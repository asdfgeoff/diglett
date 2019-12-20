""" Functions related to generating new predictive features on a dataset before fitting an ML model. """

from typing import Tuple
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from .display import print_header_with_lines
from .wrangle import categorical_fillna


def make_comparison_bools(df: pd.DataFrame, comparisons: dict) -> pd.DataFrame:
    """ Assigns a float bool column to DataFrame reflecting whether a value equals another value.

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
            comparison_srs = (df[col_a] == df[col_b])
        except TypeError:
            comparison_srs = (df[col_a].astype('object') == df[col_b].astype('object'))

        with_nans = comparison_srs.where((df[col_a].isnull() == False) & (df[col_b].isnull() == False))
        output_df[output_col_name] = with_nans

    return output_df


def ordinal_encode_categoricals(X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """ Fit an OrdinalEncoder on a combined test/train dataset and return transforms on each individual dataset. """

    X_train_out, X_test_out = X_train.copy(), X_test.copy()

    X_all = pd.concat([X_train, X_test]).pipe(categorical_fillna)
    cat_cols = X_all.select_dtypes('category').dtypes.index.values.tolist()
    enc = OrdinalEncoder()
    enc.fit(X_all[cat_cols])

    X_train_out[cat_cols] = enc.transform(X_train[cat_cols].pipe(categorical_fillna))
    X_test_out[cat_cols] = enc.transform(X_test[cat_cols].pipe(categorical_fillna))

    return X_train_out, X_test_out


if __name__ == '__main__':
    pass
