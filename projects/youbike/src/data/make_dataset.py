import pandas as pd
import dask.dataframe as dd


def resample_df(df, freq=None):
    return df.resample(freq).mean() if freq else df


def _add_date_column(df, date_str):
    date_column = []
    date = pd.to_datetime(date_str)
    for index, _ in df.iterrows():
        date_with_hour = date + pd.DateOffset(hours=index)
        date_column.append(date_with_hour)

        if (index + 1) % 24 == 0:
            date += pd.DateOffset(days=1)
    df['日期'] = date_column
    return df


def get_weather_history_data(year=2018):
    weather_history_data_path = f"drive/My Drive/taipei-weather-{year}/*.csv"

    col_names = [
        '氣溫(℃)',
        '相對溼度(%)',
        '風速(m/s)',
        '風向(360degree)',
        '降水量(mm)'
    ]

    df = (dd.read_csv(
        weather_history_data_path,
        usecols=[3, 5, 6, 7, 10],
        header=0,
        names=col_names,
        na_values=['/', 'X', 'T', 'V', '...'],
        assume_missing=True
    )
        .compute()
    )

    # add datetime
    df = _add_date_column(df, f"1/1/{year}")

    # set datetime as index
    df = df.set_index('日期')

    # imputation
    df = df.fillna(method='ffill')

    return df


def get_air_history_data(year=2018):
    air_history_data_path = f"drive/My Drive/taipei-air-{year}.csv"

    usecols_indices = [i for i in range(4, 30)]
    df = (pd.read_csv(air_history_data_path,
                      usecols=usecols_indices,
                      na_values=['x']))
    # remove redundant rows
    df = df.iloc[1:2969]

    # reverse order, since 12/31 is the first row, 1/1 is the last row
    df['監測日期'] = pd.to_datetime(df['監測日期'])
    df = df.sort_values('監測日期')

    # imputation
    df = df.fillna(method='ffill')

    df = df.set_index('監測日期')

    # make air_df
    date_range = pd.date_range(start=f"1/1/{year}", end=f"6/15/{year}")
    air_df = pd.DataFrame()
    for date in date_range:
        date_str = str(date).split(' ')[0]
        if date_str in df.index:
            sub_df = df.loc[date_str].T
            headers = sub_df.iloc[0]
            sub_df = pd.DataFrame(sub_df.values[1:], columns=headers)

            # add datetime
            sub_df = _add_date_column(sub_df, date_str)

            if air_df.empty:
                air_df = sub_df
            else:
                air_df = pd.concat([air_df, sub_df], sort=True)

    air_df = air_df.set_index('日期')

    mapper = {
        '小時風向值  ()': '小時風向值',
        '細懸浮微粒 PM 2.5  (μg/m 3 )': '細懸浮微粒(μg/m^3)',
        '總碳氫化合物 THC (ppm)': '總碳氫化合物(ppm)',
        '小時風速值 WS_HR (m/sec)': '小時風速值(m/sec)',
        '小時風向值 WD_HR (degrees)': '小時風向值(degrees)',
        '風向 WIND_DIREC (degrees)': '風向(degrees)',
        '相對濕度 RH (percent)': '相對濕度(percent)',
        '懸浮微粒 PM 10  (μg/m 3 )': '懸浮微粒(μg/m^3)',
        '甲烷 CH4 (ppm)': '甲烷(ppm)',
        '風速 WIND_SPEED (m/sec)': '風速(m/sec)',
        '非甲烷碳氫化合物 NMHC (ppm)': '非甲烷碳氫化合物(ppm)',
        '一氧化碳 CO (ppm)': '一氧化碳(ppm)',
        '二氧化氮 NO2 (ppb)': '二氧化氮(ppb)',
        '氮氧化物 NOx (ppb)': '氮氧化物(ppb)',
        '二氧化硫 SO2 (ppb)': '二氧化硫(ppb)',
        '臭氧 O3 (ppb)': '臭氧(ppb)',
        '溫度 AMB_TEMP (℃)': '溫度(℃)'
    }
    air_df = air_df.rename(columns=mapper)

    '''
    經過相關性分析：
    非甲烷碳氫化合物與甲烷相關係數過高，去除非甲烷碳氫化合物
    溫度,相對濕度,風向值,風速值已出現在天氣資料中，故去除
    '''
    usecols = [
        '細懸浮微粒(μg/m^3)',
        '總碳氫化合物(ppm)',
        '懸浮微粒(μg/m^3)',
        '甲烷(ppm)',
        '一氧化碳(ppm)',
        '二氧化氮(ppb)',
        '氮氧化物(ppb)',
        '二氧化硫(ppb)',
        '臭氧(ppb)'
    ]
    return air_df[usecols]


def get_weather_air_history_data(year=2018):
    weather_df = get_weather_history_data(year=year)
    air_df = get_air_history_data(year=year)

    weather_air_df = pd.concat([air_df, weather_df], axis=1, sort=True)
    weather_air_df = weather_air_df.fillna(method='ffill')

    return weather_air_df


def get_youbike_history_data(stop_no=None):
    FILE_PATHS = [
        'drive/My Drive/youbike-history-data-1.csv.zip',
        'drive/My Drive/youbike-history-data-2.csv.zip'
    ]

    FIELDS_LIST = [
        'stop_no',
        'stop_name',
        'total_number',
        'current_number',
        'stop_area',
        'update_time',
        'lat',
        'lng',
        'address',
        'stop_area_en',
        'stop_name_en',
        'address_en',
        'vacancy_number',
        'status',
        'batch_update_time',
        'db_update_time',
        'update_info_time',
        'update_info_date'
    ]

    FIELDS_TO_KEEP = [
        'stop_no',
        'stop_name',
        'stop_area',
        'lat',
        'lng',
        'total_number',
        'current_number',
        'vacancy_number',
        'status',
        'db_update_time'
    ]

    read_csv_func = partial(pd.read_csv, names=FIELDS_LIST)
    df = pd.concat(map(read_csv_func, FILE_PATHS), sort=True)
    df = df[FIELDS_TO_KEEP]
    df['db_update_time'] = pd.to_datetime(df['db_update_time'])
    df = df[df['status'] == 1]  # enabled

    if stop_no:
        df = (df[df['stop_no'] == stop_no]
              .sort_values('db_update_time')
              .set_index('db_update_time'))
    else:
        df = (df.groupby('stop_no')
                .apply(pd.DataFrame.sort_values, 'db_update_time')
                .set_index(['stop_no', 'db_update_time']))

    return df


def get_weather_air_df(path='drive/My Drive/1.0-weather-air-history-data-taipei-df.pkl'):
    return pd.read_pickle(path)


def get_youbike_df(path='drive/My Drive/1.0-youbike-history-data-186-df.pkl'):
    return pd.read_pickle(path)


def get_youbike_integration_df(youbike_df=None, weather_air_df=None):
    if not youbike_df:
        youbike_df = get_youbike_df()
    if not weather_air_df:
        weather_air_df = get_weather_air_df()

    # merge two dataframes and do some preprocessings
    # - imputation
    # - filter out redundant fields
    # - rename columns
    fields_needed = [
        '可借車數',
        '細懸浮微粒(μg/m^3)',
        '總碳氫化合物(ppm)',
        '懸浮微粒(μg/m^3)',
        '甲烷(ppm)',
        '一氧化碳(ppm)',
        '二氧化氮(ppb)',
        '氮氧化物(ppb)',
        '二氧化硫(ppb)',
        '臭氧(ppb)',
        '氣溫(℃)',
        '相對溼度(%)',
        '風速(m/s)',
        '風向(360degree)',
        '降水量(mm)'
    ]

    rename_mapper = {
        'current_number': '可借車數',
    }

    df = (pd.merge(youbike_df, weather_air_df,
                   how='outer', left_index=True,
                   right_index=True, sort=True)
          .fillna(method='ffill')
          .fillna(method='bfill')
          .rename(columns=rename_mapper)
          )

    return df[fields_needed]
