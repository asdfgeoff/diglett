""" Useful decorators for troubleshooting data transformation pipelines and asserting assumptions.

Inspired by Tom Augspurger's package engarde: https://github.com/engarde-dev/engarde

"""

import time
import functools
from typing import Callable
import numpy as np


def describe_io(func: Callable) -> Callable:
    """ Describe the shape of the input shape, output shape, and time of a pandas pipe function. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pre_shape = str(args[0].shape)
        result = func(*args, **kwargs)
        try:
            post_shape = str(result.shape)
        except AttributeError:
            post_shape = 'NA'
        print(f'{func.__name__:40} IN: {pre_shape:15} OUT: {post_shape:15}')
        return result
    return wrapper


def timeit(func: Callable) -> Callable:
    """ Display the time taken to complete a pandas operation and the relative time by input size. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.time()
        n_rows = args[0].shape[0]
        result = func(*args, **kwargs)
        te = time.time()
        sec = te - ts
        sec_per_mille = (sec / n_rows) * 1000
        print(f'{func.__name__:40} TOTAL TIME: {sec:5.2f}s \t PER THOUSAND:{sec_per_mille:5.2f}s')
        return result
    return wrapper


def columns_exist(columns: list) -> Callable:
    """ Verify that a list of columns exist in the input DataFrame.

    The function being decorated should accept a pandas.DataFrame object as first argument
    and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.

    """

    def real_decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            missing_columns = set(columns) - set(args[0].columns)
            if len(missing_columns) > 0:
                print(f'Missing expected columns: {missing_columns}')
            result = func(*args, **kwargs)
            return result
        return wrapper
    return real_decorator


def no_object_dtypes(func: Callable) -> Callable:
    """ Verify that all columns of the output DataFrame have a dtype other than 'Object'.

    The function being decorated should accept a pandas.DataFrame object as first argument
    and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        object_columns = [c for c, d in result.dtypes.items() if d == np.dtype('object')]
        if len(object_columns) > 0:
            raise TypeError('Remaining columns of dtype object: {}'.format(object_columns))
    return wrapper


def no_additional_nulls(func: Callable) -> Callable:
    """ Warn if the number of nulls in a DataFrame has increased during transformation.

    The function being decorated should accept a pandas.DataFrame object as first argument
    and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.

    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nulls_before = args[0].isnull().sum().sum()
        result = func(*args, **kwargs)
        nulls_after = result.isnull().sum().sum()
        if nulls_after > nulls_before:
            raise ValueError('There are more nulls in the output than the input dataframe. ({} before vs {} after)'.format(nulls_before, nulls_after))
        return result
    return wrapper


def same_num_rows(func):
    """ Ensure that a DataFrame transformation function returns the same number of rows as its input.

    The function being decorated should accept a pandas.DataFrame object as first argument
    and also return a DataFrame object, making it a valid function for the DataFrame.pipe() method.

    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        num_rows_before = args[0].shape[0]
        result = func(*args, **kwargs)
        num_rows_after = result.shape[0]
        if num_rows_before != num_rows_after:
            raise ValueError(f'The number of rows has changed between input ({num_rows_before} and output ({num_rows_after}).')
        return result
    return wrapper

if __name__ == '__main__':
    pass
