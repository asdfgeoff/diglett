import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


__all__ = ['plot_histogram_with_summary_stats', 'plot_two_hists', 'discrete_hist']

from .legos import basic_chart

@basic_chart()
def plot_histogram_with_summary_stats(fig, ax, data: pd.Series, clip_upper=None, *args, **kwargs):
    """ """

    if isinstance(data, pd.Series):
        pass
    elif isinstance(data, np.ndarray):
        data = pd.Series(data)
    else:
        raise ValueError('Input data must be NumPy array or pandas Series.')

    # clip data (if necessary)
    to_viz = data.clip(upper=clip_upper)

    # plot core data
    sns.histplot(to_viz, bins=50, ax=ax, *args, **kwargs)

    # annotate
    fig.canvas.draw()  # necessary to get non-empty ticks
    annotate_distplot(ax, data)

    # misc formatting

    return fig, ax

@basic_chart()
def discrete_hist(fig, ax, data: pd.Series, clip_upper=None, annotate=False, *args, **kwargs):
    """ """

    # clip data (if necessary)
    to_viz = data.clip(upper=clip_upper)
    
    n = to_viz.nunique()
    x_min, x_max = to_viz.min(), to_viz.max()

    # plot core data
    ax = sns.distplot(
        to_viz,
        bins=np.arange(n+0.5)-0.5+x_min,
        ax=ax,
        kde=False, 
        norm_hist=True,
        hist_kws={'edgecolor': 'white', 'rwidth': 0.9},
        *args, **kwargs)

    # formatting
    ax.xaxis.set_ticks(np.arange(x_min, x_max+1, 1))
    ax.set_xlim([x_min-0.5, x_max+0.5])
    ax.set_xlabel('')

    if annotate:
        annotate_distplot(ax, data)
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0, decimals=0))
    
    # replace final label with +
    fig.canvas.draw()  # necessary to get non-empty ticks
    labels = [obj.get_text() for obj in ax.get_xticklabels()]
    labels[-1] += '+'
    ax.set_xticklabels(labels)

    return fig, ax


def annotate_distplot(ax, data, mean_color='grey', median_color='pink', pad=0.01, log_transform=False) -> None:
    """ Draw lines and annotate text on a histogram to indicate mean and median values. """

    text_defaults = dict(va='center', ha='left', transform=ax.transAxes)
    mean = mean_label = np.mean(data)
    median = median_label = np.median(data)
    if log_transform:
        mean, mean_label = np.log10(mean), mean
        median, median_label = np.log10(median), median

    # annotate mean
    ax.axvline(mean, linestyle='--', color=mean_color)
    rel_pos = ax.transLimits.transform((mean, 0))[0]
    ax.text(rel_pos+pad, 0.95, f'Mean: {mean_label:.0f}', color=mean_color, **text_defaults)

    # annotate median
    ax.axvline(median, linestyle='--', color=median_color)
    rel_pos = ax.transLimits.transform((median, 0))[0]
    ax.text(rel_pos+pad, 0.88, f'Median: {median_label:.0f}', color=median_color, **text_defaults)


def plot_log_histogram_with_summary_stats(data):
    """ """

    # plot core date
    fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
    log_data = np.log10(data)
    sns.distplot(log_data, bins=50)

    # annotate
    fig.canvas.draw()  # necessary to get non-empty ticks
    annotate_distplot(ax, data, log_transform=True)

    # misc formatting
    labels = [obj.get_text() for obj in ax.get_xticklabels()]
    new_labels = [10**int(x.replace('−', '-')) for x in labels]
    _ = ax.set_xticklabels(new_labels)
    _ = ax.set_xlabel('Total messages (log)')
    _ = ax.yaxis.set_ticklabels([])


def plot_two_hists(data: dict, *args, **kwargs):
    """
    Args:
        data: {name, pd.Series} pairs
    """

    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    
    for k, v in data.items():
        sns.distplot(v, label=k, ax=ax, *args, **kwargs)
        
    plt.legend()

if __name__ == '__main__':
    pass
