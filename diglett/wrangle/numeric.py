import pandas as pd


def winsorize(srs: pd.Series, lower=0, upper=0.99, verbose=True) -> pd.Series:
    """Winsorize a series at specified quantiles, and print info to stdout for debugging."""
    lower_val, upper_val = srs.quantile([lower, upper]).tolist()
    trimmed = srs.clip(lower=lower_val, upper=upper_val)

    if verbose:
        print(f'Winsorizing {srs.name} to range: [{lower_val:.2f}, {upper_val:.2f}]')
        print(f'Previous mean:\t {srs.mean():.2f}')
        print(f'New mean:\t {trimmed.mean():.2f}', '\n')

    return trimmed


def multi_moving_average(df, ds_col='ds', seg_col='dim', num_col='num_', days=7):
    return (
        df.set_index(ds_col)
        .sort_index()
        .groupby(seg_col)
        .rolling(window=days)
        .mean()
        .dropna()
        .reset_index()
        .reindex([ds_col, seg_col, num_col], axis=1)
    )


if __name__ == '__main__':
    pass
