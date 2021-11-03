"""Tests related to insist sub-module."""

import pandas as pd
import pytest

from diglett.insist import average_greater_than, less_than_pct_null, more_than_pct_unique, no_nulls


@pytest.fixture
def input_df() -> pd.DataFrame:
    """Fixture to return an example pandas DataFrame."""
    return pd.DataFrame(
        {
            'A': [1, 2, 3, 4],
            'B': [1, 2, 3, None],
            'C': [1, 2, None, None],
            'D': [1, 1, 2, 3],
            'E': [0.9, 0.9, 0.8, 0.1],
        }
    )


def test_no_nulls_all_cols(input_df: pd.DataFrame):
    """Succeeds if no_nulls() returns specific HTML."""

    expected = (
        '<div class="alert alert-danger" style="margin: 5px;">'
        + '☠️ &nbsp; More than 0% null values in cols: B, C</div>'
    )

    actual = input_df.pipe(no_nulls, return_alert=True).data

    assert actual == expected


def test_no_nulls_specific_col(input_df: pd.DataFrame):
    """Succeeds if no_nulls(cols) returns specific HTML."""

    expected = (
        '<div class="alert alert-success" style="margin: 5px;">'
        + '✅ &nbsp; Less than 0% null values in cols: A</div>'
    )

    actual = input_df.pipe(no_nulls, cols=['A'], return_alert=True).data

    assert actual == expected


def test_less_than_pct_null(input_df: pd.DataFrame):
    """Succeeds if less_than_pct_null(cols, pct) returns specific HTML."""

    expected = (
        '<div class="alert alert-success" style="margin: 5px;">'
        + '✅ &nbsp; Less than 50% null values in cols: B</div>'
    )

    actual = input_df.pipe(less_than_pct_null, cols=['B'], pct=0.50, return_alert=True).data

    assert actual == expected


def test_more_than_pct_unique_fail(input_df: pd.DataFrame):
    """Succeeds if more_than_pct_unique(col) returns specific HTML."""

    expected = (
        '<div class="alert alert-danger" style="margin: 5px;">'
        '☠️ &nbsp; Cardinality: 75.00% of values in D are unique. Threshold set is 99.00%.</div>'
    )

    actual = input_df.pipe(more_than_pct_unique, col='D', return_alert=True).data

    assert actual == expected


def test_more_than_pct_unique_success(input_df: pd.DataFrame):
    """Succeeds if more_than_pct_unique(col) returns specific HTML."""

    expected = (
        '<div class="alert alert-success" style="margin: 5px;">'
        '✅ &nbsp; Cardinality: 100.00% of values in A are unique. Threshold set is 99.00%.</div>'
    )
    actual = input_df.pipe(more_than_pct_unique, col='A', return_alert=True).data

    assert actual == expected


def test_average_greater_than(input_df: pd.DataFrame):
    """Succeeds if average_greater_than(col, threshold) returns specific HTML."""

    expected = (
        '<div class="alert alert-success" style="margin: 5px;">'
        '✅ &nbsp; Avg value of E is 67.50%. Threshold is 50.00%.</div>'
    )
    actual = input_df.pipe(average_greater_than, col='E', threshold=0.5, return_alert=True).data

    assert actual == expected
