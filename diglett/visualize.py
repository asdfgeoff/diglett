""" Functions for performing visualizations with matplotlib and seaborn. """
from typing import Tuple, Callable
from warnings import warn
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import seaborn as sns
from IPython.core.display import display
from .display import header


def mpl_boilerplate(shape: Tuple[int, int] = (6, 4),
                    left_title: bool = False,
                    y_axis: bool = True,
                    grid: bool = False,
                    legend: bool = True) -> None:
    """ Decorator to perform boilerplate matplotlib formatting.
    Target plot function must accept fig, ax as first args and also return them.

    Example:
        @mpl_boilerplate(grid=True, legend=False)
        def my_plot(data, *args, **kwargs):

            try:
                fig, ax = kwargs['fig'], kwargs['ax']
            except KeyError:
                fig, ax = plt.subplots()

            ax.plot(data)

            return fig, ax

    Args:
        shape: size of matplotlib figure (width, height)
        left_title: whether to left-align the title
        y_axis: whether to show the y-axis
        grid: whether to display grid lines
        legend: whether to display legend

    """

    def real_decorator(func):
        def wrapper(*args, **kwargs):
            # Pre-plot config
            mpl.rcParams.update({'font.size': 14})
            fig, ax = plt.subplots(figsize=shape, dpi=100)
            fig.set_facecolor('white')

            # Run the primary plot
            fig, ax = func(*args, **kwargs, fig=fig, ax=ax)

            # Key formatting
            if 'title' in kwargs:
                if left_title:
                    ax.text(0, 1.08, kwargs['title'], size='large', transform=ax.transAxes)
                else:
                    ax.text(0.5, 1.08, kwargs['title'], size='large', transform=ax.transAxes, horizontalalignment='center')
                del kwargs['title']
            if 'subtitle' in kwargs:
                ax.text(0, 1.04, kwargs['subtitle'], size='medium', color='grey', transform=ax.transAxes)
                del kwargs['subtitle']
            if 'ylabel' in kwargs:
                ax.set_ylabel(kwargs['ylabel'], labelpad=10)
                del kwargs['ylabel']
            if 'xlabel' in kwargs:
                ax.set_xlabel(kwargs['xlabel'], labelpad=10)
                del kwargs['xlabel']

            # Misc formatting
            if legend:
                plt.legend()

            if not y_axis:
                ax.get_yaxis().set_visible(False)

            if grid:
                ax.grid(which='major', color='black', linestyle='--', alpha=0.1)
            else:
                ax.grid(False)

            plt.show()

        return wrapper

    return real_decorator


@mpl_boilerplate(y_axis=False, legend=False, grid=False)
def clipped_distplot(srs: pd.Series, quantile: float = 0.99, **kwargs):
    """ Plot a seaborn distplot with maximum values clipped at some quantile. Compatible with @mpl_boilerplate decorator. """
    try:
        fig, ax = kwargs['fig'], kwargs['ax']
    except KeyError:
        fig, ax = plt.subplots()

    to_viz = srs.clip(upper=srs.quantile(quantile))
    sns.distplot(to_viz, kde=False)

    return fig, ax


def sorted_external_legend(func):
    """ Display a legend on the outer right edge of the figure which is sorted by final value. """

    def wrapper(fig, ax, viz_df, *args, **kwargs):
        # Run the primary plot
        fig, ax = func(fig, ax, viz_df, *args, **kwargs)
        # Format legend
        final_values = {k: v[v.last_valid_index()] for k, v in viz_df.items()}
        handles, labels = ax.get_legend_handles_labels()
        handles_dict = {str(l): h for h, l in zip(handles, labels)}
        ordered_labels = [str(x) for x in sorted(final_values, key=final_values.get, reverse=True)]
        ordered_handles = [handles_dict[l] for l in ordered_labels]
        leg = plt.legend(ordered_handles, ordered_labels, loc='upper left', bbox_to_anchor=(1, 1.01))
        for legobj in leg.legendHandles:
            legobj.set_linewidth(5.0)
        return fig, ax

    return wrapper


def display_insight(df: pd.DataFrame,
                    fmt: str = None,
                    title: str = '',
                    subtitle: str = '',
                    assertion: Callable = None) -> None:
    """ Display a pandas DataFrame as a presentable display_insight.

    Args:
        df: The table to be displayed
        fmt: String representation of formatting to apply to dataframe output (e.g. {:.0%} for percentages )
        title: The key takeaway or display_insight from the table
        subtitle: A more objective description of the table contents
        assertion: A lambda statement to check the validity of the display_insight against the contents of the dataframe

    """
    if title:
        header(title, size=3)
    if subtitle:
        split = '<br>'.join(wrap(subtitle, width=60))
        header(split, size=7)

    if fmt:
        display(df.style.format(fmt))

    else:
        display(df)

    if assertion:
        if not assertion(df):
            warn('This insight may no longer be true!')


if __name__ == '__main__':
    pass
