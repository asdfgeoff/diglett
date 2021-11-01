""" Functions related to joinging/merging datasets. """

from IPython.core.display import display
import pandas as pd

# flake8: noqa: DAR101,DAR201,DAR401
def verbose_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    left_on: str = None,
    right_on: str = None,
    left_index: bool = False,
    right_index: bool = False,
    *args,
    **kwargs,
) -> pd.DataFrame:
    """Wraps pd.merge function to provide a visual overview of cardinality between datasets.

    Specify both (left_on, right_on) or (left_index, right_index) arguments.

    """

    if left_on and right_on:
        left_vals = left[left_on]
        right_vals = right[right_on]
    elif left_index and right_index:
        left_vals = left.index
        right_vals = right.index
    else:
        raise ValueError('Function must take parameters: left_on+right_on or left_index+right_index.')

    # print cardinality diagnostics
    is_unique_left = '❌'
    is_unique_right = '❌'
    if left_vals.nunique() == left_vals.shape[0]:
        is_unique_left = '✅'
    if right_vals.nunique() == right_vals.shape[0]:
        is_unique_right = '✅'
    print(f'Unique keys: ({is_unique_left}, {is_unique_right})')

    # print null diagnostics
    left_nulls = left_vals.isnull().sum()
    right_nulls = right_vals.isnull().sum()
    print(f'Nulls: ({left_nulls}, {right_nulls})')

    diag = pd.merge(
        left,
        right,
        left_on=left_on,
        right_on=right_on,
        left_index=left_index,
        right_index=right_index,
        how='outer',
        indicator=True,
    )

    display(
        diag['_merge']
        .value_counts()
        .reindex(['left_only', 'both', 'right_only'])
        .rename('Total')
        .to_frame()
        .assign(Pct=lambda x: x['Total'] / x['Total'].sum())
        .style.format({'Pct': '{:.2%}'})
    )

    return pd.merge(
        left, right, left_on=left_on, right_on=right_on, left_index=left_index, right_index=right_index, *args, **kwargs
    )
