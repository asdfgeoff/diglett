"""Tests related to the utils sub-module."""

import re
from textwrap import dedent

import pandas as pd

from diglett import utils


def test_describe_decorator(capsys):
    """Check that the describe() decorator outputs to stdout in the expected manner."""
    input_df = pd.DataFrame({'dim_A': list('ABCABC'), 'num_1': range(1, 7)})

    @utils.describe
    def test_func(df):
        return df.groupby('dim_A')['num_1'].sum()

    _ = test_func(input_df)
    actual = capsys.readouterr().out.strip('\n')

    expected_pattern = (
        r'test_func\n\s+Shape: \(6, 2\) → \(3,\)\n\s+Time: \d\.\d{2}s \(0.\d{2}s \/ 1k\)'
    )

    assert re.search(expected_pattern, actual)


def test_text_header(capsys):
    """Check that text_header() outputs to stdout in the expected manner."""
    utils.text_header('Meow')

    expected = """
    ----
    Meow
    ----
    """

    actual = capsys.readouterr().out

    assert actual.strip('\n') == dedent(expected).strip('\n')
