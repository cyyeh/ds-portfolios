import pandas as pd
import matplotlib.pyplot as plt


def draw_line_plot_by_column(df, font_prop='', color='white', label_size=14, title_size=16, fig_size=(12, 8)):
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


def draw_heatmap_by_column(df, font_prop='', color='white', label_size=14, fig_size=(12, 12)):
    f = plt.figure(figsize=fig_size)
    plt.matshow(df.corr(), fignum=f.number)
    plt.xticks(range(df.shape[1]), df.columns, fontproperties=font_prop,
               fontsize=label_size, rotation=75, color=color)
    plt.yticks(range(df.shape[1]), df.columns,
               fontproperties=font_prop, fontsize=label_size, color=color)
    cb = plt.colorbar()
    cb.ax.tick_params(labelsize=label_size, labelcolor=color, color=color)


def plot_youbike_mean_available_number(df, freq='realtime', label_size=14, title_size=16, color='white', fig_size=(12, 8)):
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
