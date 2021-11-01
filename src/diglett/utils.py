""" Various utility functions, mostly used within the rest of the diglett module. """

import functools
import time
from typing import Any, Callable

from IPython.core.display import display, HTML


def describe(func: Callable) -> Callable:
    """Describe the shape of the input shape, output shape, and time of a pandas pipe function."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        pre_shape = str(args[0].shape)
        n_rows = args[0].shape[0]
        start_ts = time.time()

        result = func(*args, **kwargs)

        try:
            post_shape = str(result.shape)
        except AttributeError:
            post_shape = 'NA'

        end_ts = time.time()
        sec = end_ts - start_ts
        sec_per_mille = (sec / n_rows) * 1000

        print(f'{func.__name__}')
        print(f'  Shape: {pre_shape} → {post_shape}')
        print(f'  Time: {sec:.2f}s ({sec_per_mille:.2f}s / 1k)')
        return result

    return wrapper


def text_header(text: str, line_char: str = '-') -> None:
    """Sandwich a given string with an equal length line of separate characters above and below it."""
    length = len(text)
    print('', line_char * length, text, line_char * length, sep='\n')


def display_header(size: int, text: str) -> None:
    """Display an HTML header of a specified level."""
    display(HTML(f'<h{size} style="margin: 5px 0px;">{text}</h{size}>'))


h2 = functools.partial(display_header, 2)
h3 = functools.partial(display_header, 3)
h4 = functools.partial(display_header, 4)
h5 = functools.partial(display_header, 5)
h6 = functools.partial(display_header, 6)
h7 = functools.partial(display_header, 7)

if __name__ == '__main__':
    pass  # pragma: no cover
