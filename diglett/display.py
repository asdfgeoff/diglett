""" Some utility functions related to displaying data nicely in Jupyter Notebooks. """

from functools import partial
import pandas as pd
from IPython.core.display import HTML, display
from IPython.display import display_html


def n_largest_coefs(coefs: pd.Series, n: int = 10) -> pd.Series:
    """ Return the n largest absolute values from a pandas Series """
    return coefs.reindex(coefs.abs().sort_values(ascending=False).index).head(n)


def display_side_by_side(*args: pd.DataFrame) -> None:
    """ Output an array of pandas DataFrames side-by-side in a Jupyter notebook to conserve vertical space. """
    html_str = ''
    for df in args:
        html_str += df.to_html()
    display_html(html_str.replace('table', 'table style="display:inline"'), raw=True)


def print_header_with_lines(text: str, line_char: str = '-') -> None:
    """ Sandwich a given string with an equal length line of separate characters above and below it. """
    length = len(text)
    print('', line_char*length, text, line_char*length, sep='\n')


def display_header(size: int, text: str) -> None:
    """ Display an HTML header representation of a given string in a given size """
    display(HTML(f'<h{size}>{text}</h{size}>'))


h2 = partial(display_header, 2)
h3 = partial(display_header, 3)
h4 = partial(display_header, 4)
h7 = partial(display_header, 7)

if __name__ == '__main__':
    pass
