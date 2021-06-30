from warnings import warn
import pandas as pd


def verbose_merge(left, right, left_on=None, right_on=None, left_index=False, right_index=False, *args, **kwargs):
    """Wraps pd.merge function to provide a visual overview of cardinality between datasets."""

    if left_on:
        left_vals = left[left_on]
        left_name = left_on
    elif left_index:
        left_vals = left.index
        try:
            left_name = left_vals.index.name
        except AttributeError:
            left_name = 'idx'
    else:
        raise ValueError('Function must take parameer left_on or left_index.')

    left_nulls = left_vals.isnull()
    if left_nulls.sum() > 0:
        warn(f'Left join key has {left_nulls.sum()} null values ({left_nulls.mean():.0%} of values)')
    left_set = set(left_vals)

    if right_on:
        right_vals = right[right_on]
        right_name = right_on
    elif right_index:
        right_vals = right.index
        try:
            right_name = right_vals.index.name
        except AttributeError:
            right_name = 'idx'
    else:
        raise ValueError('Function must take parameer right_on or right_index.')

    right_nulls = right_vals.isnull()
    if right_nulls.sum() > 0:
        warn(f'Right join key has {right_nulls.sum()} null values ({right_nulls.mean():.0%} of values)')
    right_set = set(right_vals)

    num_left_total = len(left_set)
    pct_left_only = len(left_set - right_set) / num_left_total
    pct_left_shared = len(left_set & right_set) / num_left_total

    num_right_total = len(right_set)
    pct_right_only = len(right_set - left_set) / num_right_total
    pct_right_shared = len(right_set & left_set) / num_right_total

    num_both_total = len(left_set | right_set)
    pct_both_shared = len(left_set & right_set) / num_both_total
    pct_both_left_only = len(left_set - right_set) / num_both_total
    pct_both_right_only = len(right_set - left_set) / num_both_total

    table_str = f"""
        |{left_name.upper():^10.10}|{"LEFT":^10s}|{"INNER":^10s}|{"RIGHT":^10s}|{right_name.upper():^10.10}|
        |----------|----------|----------|----------|----------|
        |{num_left_total:^10d}|{pct_left_only:^10.0%}|{pct_left_shared:^10.0%}|          |          |
        |----------|----------|----------|----------|----------|
        |{num_both_total:^10d}|{pct_both_left_only:^10.0%}|{pct_both_shared:^10.0%}|{pct_both_right_only:^10.0%}|{num_both_total:^10d}|
        |----------|----------|----------|----------|----------|
        |          |          |{pct_right_shared:^10.0%}|{pct_right_only:^10.0%}|{num_right_total:^10d}|
        """

    print(table_str)

    return pd.merge(
        left, right, left_on=left_on, right_on=right_on, left_index=left_index, right_index=right_index, *args, **kwargs
    )
