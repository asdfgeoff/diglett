from functools import partial
from IPython.core.display import HTML, display


def n_largest_coefs(coefs, n=10):
    return coefs.reindex(coefs.abs().sort_values(ascending=False).index).head(n)


def print_header_with_lines(text: str, line_char: str='-') -> None:
    """ Sandwich a given string with an equal length line of separate characters above and below it. """
    length = len(text)
    print('', line_char*length, text, line_char*length, sep='\n')


def display_header(size, text):
    display(HTML(f'<h{size} style="margin: 5px 0px;">{text}</h{size}>'))


h2 = partial(display_header, 2)
h3 = partial(display_header, 3)
h4 = partial(display_header, 4)
h5 = partial(display_header, 5)
h6 = partial(display_header, 6)
h7 = partial(display_header, 7)

if __name__ == '__main__':
    pass
