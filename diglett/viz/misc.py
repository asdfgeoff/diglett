import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LogNorm
from .legos import basic_chart

__all__ = ['heatmap', 'multi_bar']


@basic_chart(default_figsize=(6, 6))
def heatmap(fig, ax, df: pd.DataFrame, log_transform=False, **kwargs) -> None:
    """ Wrapper for sns.heatmap with optional log transform
    
    Args:
        df: a pandas DataFrame in heatmap format (x-axis as columns, y-axis as rows)
    
    """

    df = df.copy()

    if log_transform:
        log_scale = LogNorm(vmin=(df.min().min()+1), vmax=df.max().max())
        df += 0.01
    else:
        log_scale = None
        
    ax = sns.heatmap(
        df,
        ax=ax,
        annot=True,
        cmap='Blues',
        fmt='.0f',
        cbar=False,
        norm=log_scale
    )
    
    # Post-plot formatting
    fig.canvas.draw()
    
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
        
    for tick in ax.get_yticklabels():
        tick.set_rotation(0)
    
    return fig, ax


@basic_chart()
def multi_bar(fig, ax, to_viz: dict, colors: dict=None):
    """ Plot multiple bars on a single chart
    
    Args:
        to_viz: a dict containing (label, pd.Series) pairs, with identical indices.
    
    """

    if not colors:
        colors = {}

    # verify indices are the same
    labels = list(to_viz.values())[0].index
    for srs in list(to_viz.values())[1:]:
        assert (srs.index == labels).all()
    
    x = np.arange(len(labels))
    n = len(to_viz)
    width = 0.80 / n

    # plot data
    for i, (label, data) in enumerate(to_viz.items()):
        ax.bar(x+width*i, data, width, label=label, color=colors.get(label, None))

    # format x-ticks
    plt.xticks(x+(n-1)*(width)/2, labels, horizontalalignment='right', rotation=45)
    ax.tick_params(axis=u'both', which=u'both',direction='out', length=5)
    
    plt.legend() 
    return fig, ax
    

if __name__ == '__main__':
    pass
