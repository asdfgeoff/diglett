import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.axes._axes import Axes
from typing import Tuple, Union

from .legos import basic_chart


def sorted_external_legend(fig, ax, data, line_width=None):
    """ """
    final_values = {k: v[v.last_valid_index()] for k, v in data.items()}
    handles, labels = ax.get_legend_handles_labels()
    handles_dict = {str(l): h for h, l in zip(handles, labels)}
    ordered_labels = [str(x) for x in sorted(final_values, key=final_values.get, reverse=True)]
    ordered_handles = [handles_dict[l] for l in ordered_labels]
    leg = plt.legend(
        ordered_handles,
        ordered_labels,
        loc='upper left',
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
        frameon=False
    )
    
    if line_width:
        for legobj in leg.legendHandles:
            legobj.set_linewidth(line_width)


# @basic_chart()
# def line_chart(
#     fig: Figure,
#     ax: Axes,
#     to_viz: Union[pd.Series, pd.DataFrame],
#     lower_err=None,
#     upper_err=None
#     ) -> Tuple[Figure, Axes]:
#     """"""
    
#     if isinstance(to_viz, pd.Series):
#         ax.plot(to_viz.index, to_viz.values, alpha=0.8)
#         if lower_err is not None and upper_err is not None:
#             plt.fill_between(to_viz.index, lower_err.values, upper_err.values, alpha=0.1)
#     elif isinstance(to_viz, pd.DataFrame):
#         for label, srs in to_viz.iteritems():
#             ax.plot(srs.index, srs.values, label=label, alpha=0.8)
#         sorted_external_legend(fig, ax, to_viz)
#     else:
#         raise ValueError
    
#     plt.gcf().autofmt_xdate()
    
#     return fig, ax


class LineChart:
    def __init__(
        self,
        to_viz: Union[pd.Series, pd.DataFrame],
        lower_err = None,
        upper_err = None,
        title: str = None,
        xlabel: str = None,
        ylabel: str = None,
        pct_y: bool = False,
        figsize = (6, 4),
        fig=None,
        ax=None
        ):
        """ """
        # init / prep
        if fig and ax:
            self.fig = fig
            self.ax = ax
        else:
            self.fig, self.ax = self.mpl_init(figsize)
        to_viz = to_viz.copy()

        # pre-formatting
        self.ax.grid(which='major', color='lightgrey', linestyle='--')
        if title:
            self.ax.set_title(title)
        if pct_y:
            to_viz *= 100
            if lower_err:
                lower_err *= 100
            if upper_err:
                upper_err *= 100
            ticks = mpl.ticker.FormatStrFormatter('%.2f%%')
            self.ax.yaxis.set_major_formatter(ticks)
        if ylabel:
            self.ax.set_ylabel(ylabel, size='medium', labelpad=10)
        if xlabel:
            self.ax.set_xlabel(xlabel, size='medium', labelpad=10)

        # core plotting
        if isinstance(to_viz, pd.Series):
            self.plot_single(to_viz, lower_err, upper_err)
        elif isinstance(to_viz, pd.DataFrame):
            self.plot_multiple(to_viz)
        else:
            raise ValueError

        # post-formatting
        self.fig.autofmt_xdate()

    @staticmethod
    def mpl_init(figsize):
        """ """
        mpl.rcParams.update({'font.size': 10})
        fig, ax = plt.subplots(figsize=figsize, dpi=100)
        fig.set_facecolor('white')
        return fig, ax

    def plot_single(self, to_viz, lower_err, upper_err):
        """ """
        self.ax.plot(to_viz.index, to_viz.values, alpha=0.8)
        if lower_err is not None and upper_err is not None:
            self.ax.fill_between(to_viz.index, lower_err.values, upper_err.values, alpha=0.1)

    def plot_multiple(self, to_viz):
        """ """
        for label, srs in to_viz.iteritems():
            self.ax.plot(srs.index, srs.values, label=label, alpha=0.8)
        sorted_external_legend(self.fig, self.ax, to_viz)

    def show(self):
        plt.show()

if __name__ == '__main__':
    pass
