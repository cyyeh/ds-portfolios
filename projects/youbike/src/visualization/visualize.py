import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.tseries.offsets import DateOffset

from ..data.make_dataset import resample_df

def _df_date_range_selector(df, date_range_start, date_range_end):
    if date_range_start and date_range_end:
        mask = (df.index >= date_range_start) & (df.index <= date_range_end)
    elif date_range_start:
        mask = (df.index >= date_range_start)
    else:
        mask = (df.index <= date_range_end)
    return df.loc[mask]    


def draw_line_plot_by_column(
    df, columns=None, font_prop='', color='white',
    label_size=14, title_size=16, fig_size=(12, 8),
    date_range_start=None, date_range_end=None,
    allow_null=True, hue=None, grid=True
    ):
    '''
    df: dataframe
    columns: draw specific columns, should be a list
    font_prop: fontproperties for matplotlib
    color: color for label, title
    label_size: label font size
    title_size: title font size
    fig_size: matplotlib figure size
    date_range_start: start date included
    date_range_end: end date excluded
    allow_null: allow any null values in column and will draw the plot by 
                skipping them
    hue: seaborn hue
    '''
    if date_range_start or date_range_end:
        df = _df_date_range_selector(df, date_range_start, date_range_end)
        # make sure all days exist in df selected from date_range_selector
        date_range = pd.date_range(start=date_range_start, end=date_range_end)
        df_D = resample_df(df, freq='D')
        if len(date_range) != len(df_D):
          return
    if columns:
        df = df[columns]
    if hue:
        df_hue = df[hue]

    df = df.select_dtypes(include=['float64', 'int64'])
    for column in df.columns:
        x = df.index
        y = df[column]
        if allow_null or not y.isnull().values.sum():
            plt.figure(figsize=fig_size)
            plt.xticks(color=color, fontsize=label_size)
            plt.yticks(color=color, fontsize=label_size)
            plt.title(column, fontproperties=font_prop,
                    fontsize=title_size, color=color)
            if hue:
                sns.lineplot(x, y, hue=df_hue)
                plt.legend(loc='upper right', prop=font_prop, fontsize=label_size)
            else:
                sns.lineplot(x, y)
            plt.ylabel(column, color=color, fontsize=label_size, fontproperties=font_prop)
            if grid:
                plt.grid()
            plt.show()
            print()


def draw_heatmap_by_column(
    df, font_prop='', color='white',
    label_size=14, fig_size=(12, 12),
    date_range_start=None, date_range_end=None
    ):
    '''
    df: dataframe
    font_prop: fontproperties for matplotlib
    color: color for label, title
    label_size: label font size
    fig_size: matplotlib figure size
    date_range_start: start date included
    date_range_end: end date excluded
    '''
    if date_range_start or date_range_end:
        df = _df_date_range_selector(df, date_range_start, date_range_end)
    df = df.select_dtypes(include=['float64', 'int64'])

    f = plt.figure(figsize=fig_size)
    plt.matshow(df.corr(), fignum=f.number)
    plt.xticks(range(df.shape[1]), df.columns, fontproperties=font_prop,
               fontsize=label_size, rotation=75, color=color)
    plt.yticks(range(df.shape[1]), df.columns,
               fontproperties=font_prop, fontsize=label_size, color=color)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=label_size, labelcolor=color, color=color)


def plot_youbike_mean_available_number(
    df, freq='realtime', color='white',
    label_size=14, title_size=16, fig_size=(12, 8),
    grid=True):
    '''
    df: dataframe
    freq: dataframe resample frequency
    color: color for label, title
    label_size: label font size
    title_size: title font size
    fig_size: matplotlib figure size
    '''
    freq_dict = {
        'realtime': '5 Minutes(realtime)',
        'H': 'Hour',
        'D': 'Day',
        'M': 'Month'
    }

    if freq == 'realtime':
        df_ = df
    else:
        df_ = df.resample(freq).mean()

    x = df_.index
    y = df_.current_number
    plt.figure(figsize=fig_size)
    plt.title(
        f"Youbike Mean Available Number per {freq_dict[freq]} at University of Taipei",
        color=color,
        fontsize=title_size
    )
    plt.xticks(color=color, fontsize=label_size)
    plt.yticks(color=color, fontsize=label_size)
    if grid:
        plt.grid()
    plt.plot(x, y)


def plot_available_youbike_numbers(
    df, start_date='1/1/2018', end_date='6/15/2018',
    days_per_period=7, freq=None, font_prop='',
    hue=None, grid=True
    ):
    '''
    df: dataframe
    start_date: line plot start date
    end_date: line plot end date
    days_per_period: days per figure
    freq: resample frequency for dataframe: H, D
    font_prop: fontproperties for matplotlib
    hue: seaborn hue, if freq is set, then hue will be set to None
    '''
    columns=['可借車數']
    if freq:
        hue = None
    if hue:
        columns += [hue]

    date_range = pd.date_range(start=start_date, end=end_date, freq=f"{days_per_period}D")
    for date in date_range:
        start_date = date
        end_date = date + DateOffset(days=days_per_period-1)

        start_date = str(start_date).split(' ')[0]
        end_date = str(end_date).split(' ')[0]

        draw_line_plot_by_column(
            resample_df(df, freq=freq),
            columns=columns,
            font_prop=font_prop, 
            date_range_start=start_date,
            date_range_end=end_date,
            allow_null=False,
            hue=hue,
            grid=grid
        )