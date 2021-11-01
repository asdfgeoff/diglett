import numpy as np
import pandas as pd

from diglett.transform import winsorize


def test_winsorize():
    """Check that winsorize() function returns expected min/max values from given input."""
    np.random.seed(42)

    input_srs = pd.Series(np.random.exponential(size=100))
    assert input_srs.max() == 4.33414633958732

    output_srs = winsorize(input_srs)
    assert output_srs.max() == 3.511863363802606
