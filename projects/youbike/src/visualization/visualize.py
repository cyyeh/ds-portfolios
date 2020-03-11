import pandas as pd
import matplotlib.pyplot as plt


def draw_line_plot_by_column(df, font_prop=None):
    for column in df.columns:
        plt.figure(figsize=(12, 8))
        x = df.index
        y = df[column]
        plt.xticks(color='white', fontsize=14)
        plt.yticks(color='white', fontsize=14)
        plt.title(column, fontproperties=font_prop, fontsize=16)
        plt.plot(x, y)
        plt.show()
        print()


def draw_heatmap_by_column(df, font_prop=None):
    f = plt.figure(figsize=(12, 12))
    plt.matshow(df.corr(), fignum=f.number)
    plt.xticks(range(df.shape[1]), df.columns, fontproperties=font_prop,
               fontsize=14, rotation=75, color='white')
    plt.yticks(range(df.shape[1]), df.columns,
               fontproperties=font_prop, fontsize=14, color='white')
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=14, labelcolor='white', color='white')


def plot_youbike_mean_available_number(df, freq='realtime'):
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
    plt.figure(figsize=(12, 8))
    plt.title(
        f"Youbike Mean Available Number per {freq_dict[freq]} at University of Taipei",
        color='white',
        fontsize=16
    )
    plt.xticks(color='white', fontsize=14)
    plt.yticks(color='white', fontsize=14)
    plt.plot(x, y)
