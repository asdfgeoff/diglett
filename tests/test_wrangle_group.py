from textwrap import dedent
import pandas as pd
from diglett.wrangle import group_other


def test_group_other_with_df_1d():

    input_df = pd.DataFrame({'dim_A': list('ABCDEFG'), 'num_': range(1, 8)})

    expected = """
      dim_A  num_
    0     G     7
    1     F     6
    2     E     5
    3     D     4
    4     C     3
    5     …     3
    """

    actual = group_other(input_df, n=5).to_string().strip('\n')

    print(actual)
    assert dedent(actual) == dedent(expected).strip('\n')


def test_group_other_with_df_2d():

    input_df = pd.DataFrame({'dim_A': list('ABCABCABC'), 'dim_B': list('XXXYYYZZZ'), 'num_': range(1, 10)})

    expected = """
      dim_A dim_B  num_
    0     …     …    10
    1     C     Z     9
    2     B     Z     8
    3     A     Z     7
    4     C     Y     6
    5     B     Y     5
    """

    actual = group_other(input_df, n=5).to_string().strip('\n')

    assert dedent(actual) == dedent(expected).strip('\n')


def test_group_other_with_srs():

    input_df = pd.DataFrame({'dim_A': list('ABCDEFG'), 'num_': range(1, 8)}).set_index('dim_A')['num_']

    expected = """
    dim_A
    G    7
    F    6
    E    5
    D    4
    C    3
    …    3
    """

    actual = group_other(input_df, n=5).to_string().strip('\n')

    print(actual)
    assert dedent(actual) == dedent(expected).strip('\n')
