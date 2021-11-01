"""Tests related to verbose_merge() function."""

import numpy as np
import pandas as pd

from diglett.join import verbose_merge


def test_verbose_merge(capsys):
    """Check that verbose_merge() returns some hard-coded expected outputs."""
    df_A = pd.DataFrame({'A': 1}, index=np.arange(1, 11))
    df_B = pd.DataFrame({'B': 2}, index=np.arange(1, 21, 2))

    output = verbose_merge(df_A, df_B, left_index=True, right_index=True)
    stdout = capsys.readouterr().out
    print(stdout)

    assert output.index.tolist() == [1, 3, 5, 7, 9]
    assert 'Unique keys: (✅, ✅)' in stdout
    assert 'Nulls: (0, 0)' in stdout
