""" Tests related to the eda sub-module. """

from textwrap import dedent

import pandas as pd

from diglett.eda import show_top_n


def test_show_top_n_with_df_1d():
    """ Test show_top_n() function with a one-dimensional DataFrame. """
    input_df = pd.DataFrame({'dim_A': list('ABCDEFG'), 'num_': range(1, 8)})

    expected = """
    dim_A  num_      pct_
    0     G     7  0.250000
    1     F     6  0.214286
    2     E     5  0.178571
    3     …    10  0.357143
    """

    actual = show_top_n(input_df, n=3, show_output=False).to_string().strip()

    print(actual)
    assert dedent(actual) == dedent(expected).strip()


def test_show_top_n_with_df_2d():
    """ Test show_top_n() function with two-dimensional input. """
    input_df = pd.DataFrame(
        {'dim_A': list('ABCABCABC'), 'dim_B': list('XXXYYYZZZ'), 'num_': range(1, 10)}
    )

    expected = """
    dim_A dim_B  num_      pct_
    0     C     Z     9  0.200000
    1     B     Z     8  0.177778
    2     A     Z     7  0.155556
    3     …     …    21  0.466667
    """

    actual = show_top_n(input_df, n=3, show_output=False).to_string().strip()

    assert dedent(actual) == dedent(expected).strip()


def test_show_top_n_with_srs():
    """ Test with series as input. """
    input_df = pd.DataFrame({'dim_A': list('ABCDEFG'), 'num_': range(1, 8)}).set_index('dim_A')[
        'num_'
    ]

    expected = """
    dim_A  num_      pct_
    0     G     7  0.250000
    1     F     6  0.214286
    2     E     5  0.178571
    3     …    10  0.357143
    """

    actual = show_top_n(input_df, n=3, show_output=False).to_string().strip()

    print(actual)
    assert dedent(actual) == dedent(expected).strip()
