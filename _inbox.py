def remove_value_from_multi_index_df(df: pd.DataFrame, val_to_remove: str) -> pd.DataFrame:
    """ Drop rows which contain a particular value at any level of a hierarchical index. """

    from itertools import compress
    df = df.copy()

    # get list of index levels which contain the values
    bool_mask = [val_to_remove in level_vals for level_vals in df.index.levels]
    index_levels = list(compress(df.index.names, bool_mask))

    # for each index level with that value possible, select only rows without that value
    for idx_lvl in index_levels:
        df = df.loc[lambda x: x.index.get_level_values(idx_lvl) != val_to_remove]

    return df


def keep_specific_values_of_multi_index(df: pd.DataFrame, keep_vals: str) -> pd.DataFrame:
    """ For each level of MultiIndex which contains one or more special values, select only rows with that value.

    Written for use-case of having an "all" category in non-mutually-exclusive dimensions,
    which should be used wheneever that dimension is not explicitly filtered upon.

    """

    from itertools import compress
    df = df.copy()

    # get list of index levels which contain the values
    bool_mask = [any([keep_val in level_vals for keep_val in keep_vals]) for level_vals in df.index.levels]
    index_levels = list(compress(df.index.names, bool_mask))

    # for each index level with that value possible, select only rows without that value
    for idx_lvl in index_levels:
        df = df.loc[lambda x: x.index.get_level_values(idx_lvl).isin(keep_vals)]

    return df


def collapse_non_mece_index_levels(df: pd.DataFrame, keep_vals: str) -> pd.DataFrame:
    """ For each level of MultiIndex which contains one or more special values, select only rows with that value.

    Written for use-case of having an "all" category in non-mutually-exclusive dimensions,
    which should be used wheneever that dimension is not explicitly filtered upon.

    """

    from itertools import compress
    df = df.copy()
    all_cols = df.index.names

    # get list of index levels which contain the values
    bool_mask = [any([keep_val in level_vals for keep_val in keep_vals]) for level_vals in df.index.levels]
    index_levels = list(compress(all_cols, bool_mask))

    # for each index level with that value possible, select only rows without that value
    for idx_lvl in index_levels:
        df = df.loc[lambda x: x.index.get_level_values(idx_lvl).isin(keep_vals)]

    return df.groupby(level=list(set(all_cols) - set(index_levels))).sum()