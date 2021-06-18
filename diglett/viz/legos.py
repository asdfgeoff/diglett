import functools
import matplotlib.pyplot as plt
import matplotlib as mpl


def basic_chart(default_figsize=(6, 4), grid=True):
    """ Boilerplate chart labels and axis formatting. """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Pull out formatting-related kwargs before calling function
            format_kwargs = {}
            for key in ['title', 'subtitle', 'ylabel', 'xlabel', 'hide_y', 'xlim']:
                if key in kwargs:
                    format_kwargs[key] = kwargs[key]
                    del kwargs[key]
            if 'figsize' in kwargs:
                figsize = kwargs['figsize']
                del kwargs['figsize']
            else:
                figsize = default_figsize

            # Initialize chart
            mpl.rcParams.update({'font.size': 10})
            fig, ax = plt.subplots(figsize=figsize, dpi=100)
            fig.set_facecolor('white')

            # Run the primary plot
            fig, ax = func(fig, ax, *args, **kwargs)
            err = 'Wrapped function must return a (fig, ax) pair'
            assert isinstance(fig, mpl.figure.Figure) and isinstance(ax, mpl.axes._axes.Axes), err

            # Formatting
            if 'title' in format_kwargs:
                ax.set_title(format_kwargs['title'])
                #ax.text(0, 1.08, kwargs['title'], size='xx-large', transform=ax.transAxes)
            if 'subtitle' in format_kwargs:
                ax.text(0, 1.04, format_kwargs['subtitle'], size='medium', color='grey', transform=ax.transAxes)
            if 'ylabel' in format_kwargs:
                ax.set_ylabel(format_kwargs['ylabel'], size='medium', labelpad=10)
            if 'xlabel' in format_kwargs:
                ax.set_xlabel(format_kwargs['xlabel'], size='large', labelpad=10)
            if 'hide_y' in format_kwargs and format_kwargs['hide_y']:
                ax.yaxis.set_ticklabels([])
            if 'xlim' in format_kwargs:
                ax.set_xlim(*format_kwargs['xlim'])
            if grid:
                ax.grid(which='major', color='lightgrey', linestyle='--')

            plt.show()
            
        return wrapper

    return decorator

def sorted_external_legend(line_width=None):
    """ Display a legend on the outer right edge of the figure which is sorted by final value. """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(fig, ax, data, *args, **kwargs):
            # Run the primary plot
            fig, ax = func(fig, ax, data, *args, **kwargs)

            # Format legend
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

            #plt.tight_layout()
            
            if line_width:
                for legobj in leg.legendHandles:
                    legobj.set_linewidth(line_width)
            
            return fig, ax
        return wrapper
    return decorator


@basic_chart()
def example_sub_chart(fig, ax, data, **kwargs):
    """ Example of a plotting function wrapped by basic_chart decorator. """
    ax.plot(data)
    plt.show()
    return fig, ax


# def sorted_external_legend(func):
#     """ Display a legend on the outer right edge of the figure which is sorted by final value. """
#     @functools.wraps(func)
#     def wrapper(fig, ax, data, *args, **kwargs):
#         # Run the primary plot
#         fig, ax = func(fig, ax, data, *args, **kwargs)

#         # Format legend
#         final_values = {k: v[v.last_valid_index()] for k, v in data.items()}
#         handles, labels = ax.get_legend_handles_labels()
#         handles_dict = {str(l): h for h, l in zip(handles, labels)}
#         ordered_labels = [str(x) for x in sorted(final_values, key=final_values.get, reverse=True)]
#         ordered_handles = [handles_dict[l] for l in ordered_labels]
#         leg = plt.legend(ordered_handles, ordered_labels, loc='upper left', bbox_to_anchor=(1, 1.01))
#         for legobj in leg.legendHandles:
#             print(legobj.get_linewidth())
#             legobj.set_linewidth(5.0)
#         return fig, ax

#     return wrapper