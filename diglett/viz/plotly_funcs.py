import plotly.express as px 
import pandas as pd

__all__ = ['single_line', 'multi_line']

def single_line(srs: pd.Series, title: str='', y_pct=False, return_fig=False):
    """ Use Plotly to visualize a single pandas Series """

    if not title:
        title = srs.name
    
    fig = px.line(
        srs,
        x=srs.index.tolist(),
        y=srs.tolist(),
        title=title
    )

    fig.update_xaxes(title_text='Date')
    
    if y_pct:
        fig.update_layout(yaxis_tickformat = '.2%')

    fig.show()

    if return_fig:
        return fig


def multi_line(df: pd.DataFrame, title: str='', return_fig=False, log_y=False):
    """ Expects input to be a DataFrame with three columns: (date, dim, metric). """

    if isinstance(df, pd.DataFrame):
        assert len(df.columns.values) == 3, 'Expecting three columns: (date, dim, metric)'
        x, d, y = df.columns.values
    elif isinstance(df, pd.Series):
        pass
    else:
        raise TypeError('Expecting either a pandas Series or DataFrame object as input')

    if not df['ds'].is_monotonic:
        df = df.sort_values(by='ds')

    fig = px.line(
        df,
        x=x,
        y=y,
        color=d,
        line_group=d,
        hover_name=d,
        log_y=log_y,
        title=title
    )

    fig.for_each_trace(lambda t: t.update(t.update(name=t.name.split("=")[1])))

    fig.update_xaxes(title_text=None)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="right",
        x=1
    ))

    fig.show()

    if return_fig:
        return fig

if __name__ == '__main__':
    pass
