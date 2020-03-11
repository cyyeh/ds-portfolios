import pandas as pd
import matplotlib.pyplot as plt

def _df_date_range_selector(df, date_range_start, date_range_end):
    if date_range_start and date_range_end:
        mask = (df.index >= date_range_start) & (df.index <= date_range_end)
    elif date_range_start:
        mask = (df.index >= date_range_start)
    else:
        mask = (df.index <= date_range_end)
    return df.loc[mask]    

def draw_line_plot_by_column(
    df, font_prop='', color='white',
    label_size=14, title_size=16, fig_size=(12, 8),
    date_range_start=None, date_range_end=None
    ):
    '''
    df: dataframe
    font_prop: fontproperties for matplotlib
    color: color for label, title
    label_size: label font size
    title_size: title font size
    fig_size: matplotlib figure size
    date_range_start: start date included
    date_range_end: end date included
    '''
    if date_range_start or date_range_end:
        df = _df_date_range_selector(df, date_range_start, date_range_end)

    for column in df.columns:
        plt.figure(figsize=fig_size)
        x = df.index
        y = df[column]
        plt.xticks(color=color, fontsize=label_size)
        plt.yticks(color=color, fontsize=label_size)
        plt.title(column, fontproperties=font_prop,
                  fontsize=title_size, color=color)
        plt.plot(x, y)
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
    date_range_end: end date included
    '''
    if date_range_start or date_range_end:
        df = _df_date_range_selector(df, date_range_start, date_range_end)

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
    label_size=14, title_size=16, fig_size=(12, 8)):
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
    plt.plot(x, y)
