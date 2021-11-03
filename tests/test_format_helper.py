"""Tests related to format_helper() function."""

import pandas as pd
import pytest

from diglett.output import format_helper


@pytest.fixture
def input_df() -> pd.DataFrame:
    """Create a DataFrame to use as input for tests."""
    return pd.DataFrame({'num_': [1, 2, 3, 4], 'pct_': [0.9, 0.9, 0.8, 0.1]})


def test_format_helper_df_input(input_df: pd.DataFrame):
    """Test base call of format_helper(), with minimal arguments."""
    styler = input_df.pipe(format_helper, int_cols=None, return_output=True)
    assert styler.data.sum().sum() == 12.7
    if pd.__version__ >= '1.3.0':
        assert styler.hide_index_ == True


def test_format_helper_explicit_cols(input_df: pd.DataFrame):
    """Test format_helper() with explicit columns set."""
    styler = input_df.pipe(
        format_helper,
        int_cols=['num_'],
        pct_cols=['pct_'],
        monospace=False,
        hide_index=False,
        return_output=True,
    )
    assert styler.data.sum().sum() == 12.7
    if pd.__version__ >= '1.3.0':
        assert styler.hide_index_ == False


def test_format_helper_styler_input(input_df: pd.DataFrame):
    """Test format_helper() when input is a pandas Styler object."""
    styler_input = input_df.pipe(format_helper, return_output=True)
    styler = styler_input.pipe(format_helper, return_output=True)
    assert styler.data.sum().sum() == 12.7
    if pd.__version__ >= '1.3.0':
        assert styler.hide_index_ == True
