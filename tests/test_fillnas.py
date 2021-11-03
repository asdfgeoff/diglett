""" Test the fillnas() function. """

import pandas as pd
import pytest

from diglett.transform import fillnas


@pytest.fixture
def input_df():
    """ Create a dummy DataFrame with columns: (A, B, C). """
    return pd.DataFrame({'A': [1, 2, 3, None], 'B': [1, None, None, 4], 'C': [None, 2, 3, 4]})


def test_fillnas_all_with_zero(input_df):
    """ Basic test case. """
    output = fillnas(input_df)
    assert output.isnull().sum().sum() == 0
    assert (output == 0).sum().sum() == 4


def test_fillnas_subset_with_zero(input_df):
    """ Test with subset=['B', 'C'] argument. """
    output = fillnas(input_df, subset=['B', 'C'])
    assert output.isnull().sum().sum() == 1
    assert (output == 0).sum().sum() == 3
