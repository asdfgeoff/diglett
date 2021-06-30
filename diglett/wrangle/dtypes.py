import numpy as np
import pandas as pd


def infer_dtypes(input_df: pd.DataFrame, categorical_threshold=0.01) -> pd.DataFrame:
    """Attempt to coerce dtypes to be numerical, datetime, or categorical rather than object.

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


def cast_cols_to_dtype(df: pd.DataFrame, cols: list, dtype: str) -> pd.DataFrame:
    """Friendly with DataFrame.pipe() chain."""
    df = df.copy()
    df.loc[:, cols] = df.loc[:, cols].astype(dtype)
    return df


def cast_bools_to_float(df):
    """Hard-codes booleans as floats, necessary for CatBoost."""
    bool_cols = set((df.dtypes == bool).loc[lambda x: x == True].index)
    output_df = df.copy()
    for col in bool_cols:
        output_df[col] = output_df[col].astype(float)

    return output_df


if __name__ == '__main__':
    pass
