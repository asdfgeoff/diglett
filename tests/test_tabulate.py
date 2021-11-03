""" Tests for the tabulate() function. """

import pandas as pd
import pytest

from diglett.eda import tabulate


@pytest.fixture
def input_df():
    """ Create an input DataFrame with cols: (dim_A, dim_B, num_). """
    return pd.DataFrame(
        {'dim_A': list('ABCABCABC'), 'dim_B': list('XXXYYYZZZ'), 'num_': range(1, 10)}
    )


def test_tabulate_default(input_df):
    """ Basic test case. """
    output = tabulate(input_df, return_output=True)
    print(output)
    assert output.sum().sum() == 180
    assert output.columns.tolist() == ['Z', 'Y', 'X', 'All']
    assert output.index.tolist() == ['C', 'B', 'A', 'All']


def test_tabulate_normalized(input_df):
    """ Test with normalize=True argument. """
    output = tabulate(input_df, normalize=True, return_output=True)
    print(output)
    assert output.sum().sum() == 4.0
    assert output.columns.tolist() == ['Z', 'Y', 'X', 'All']
    assert output.index.tolist() == ['C', 'B', 'A', 'All']


def test_tabulate_unsorted(input_df):
    """ Test with sorted=False argument. """
    output = tabulate(input_df, sorted=False, return_output=True)
    print(output)
    assert output.sum().sum() == 180
    assert output.columns.tolist() == ['X', 'Y', 'Z', 'All']
    assert output.index.tolist() == ['A', 'B', 'C', 'All']
