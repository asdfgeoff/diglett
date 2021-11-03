""" Tests related to multi_moving_average() function. """

import pandas as pd
import pytest

from diglett.transform import multi_moving_average


@pytest.fixture
def input_df():
    """ Create an input DataFrame. """
    return pd.DataFrame(
        {
            'ds': pd.date_range(start='2021-01-01', periods=4).repeat(3),
            'dim_A': list('ABCABCABCABC'),
            'num_A': range(1, 13),
            'num_B': range(13, 1, -1),
        }
    ).set_index(['ds', 'dim_A'])


def test_mma_correct_order(input_df):
    """ Test with input index levels in correct order. """
    output_df = multi_moving_average(input_df)

    assert output_df.sum().sum() == 168
    assert output_df.index.names == ['ds', 'dim_A']


@pytest.mark.xfail(raises=AssertionError)
def test_mma_incorrect_order(input_df):
    """ Test with input index levels in incorrect order. """
    _ = multi_moving_average(input_df.swaplevel())
