"""Test the reindex_by_sum() function."""

import pandas as pd
import pytest

from diglett.eda import tabulate
from diglett.transform import reindex_by_sum


@pytest.fixture
def input_df():
    """ Create an input DataFrame with cols: (dim_A, dim_B, num_). """
    return pd.DataFrame(
        {'dim_A': list('ABCABCABC'), 'dim_B': list('XXXYYYZZZ'), 'num_': range(1, 10)}
    ).pipe(tabulate, sorted=False, return_output=True)


def test_reindex_by_sum_axis_0(input_df):
    """ Test with axis=0 argument. """
    output = reindex_by_sum(input_df, axis=0)
    assert output.columns.tolist() == ['X', 'Y', 'Z', 'All']
    assert output.index.tolist() == ['All', 'C', 'B', 'A']


def test_reindex_by_sum_axis_1(input_df):
    """ Test with axis=1 argument. """
    output = reindex_by_sum(input_df, axis=1)
    assert output.columns.tolist() == ['All', 'Z', 'Y', 'X']
    assert output.index.tolist() == ['A', 'B', 'C', 'All']


def test_reindex_by_sum_axis_0_margin(input_df):
    """ Test with axis=0, margin_col='All' arguments. """
    output = reindex_by_sum(input_df, axis=0, margin_col='All')
    assert output.columns.tolist() == ['X', 'Y', 'Z', 'All']
    assert output.index.tolist() == ['C', 'B', 'A', 'All']


def test_reindex_by_sum_axis_1_margin(input_df):
    """ Test with axis=1, margin_col='All' arguments. """
    output = reindex_by_sum(input_df, axis=1, margin_col='All')
    assert output.columns.tolist() == ['Z', 'Y', 'X', 'All']
    assert output.index.tolist() == ['A', 'B', 'C', 'All']
