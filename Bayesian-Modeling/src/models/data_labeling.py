import pandas as pd
import scipy
import numpy as np
from tqdm import tqdm

def identify_ranges(data):
    avg_col_idx = data.columns.get_loc("New Cases/100k population")
    print(avg_col_idx)
    data['daily_growth_range'] = data.iloc[:,avg_col_idx].diff().fillna(0)
    mean = data['daily_growth_range'].mean()
    x_values = data['daily_growth_range'].values
    standard_deviation = np.std(x_values)
    x_values = np.sort(x_values)
    y_values = scipy.stats.norm(mean, standard_deviation)

    print('min : ',x_values.min(), 'max: ',x_values.max())
    median = np.median(x_values)
    st_dev = np.std(x_values)
    mini = x_values.min()
    maxi = x_values.max()
    alpha = 0.5
    while (mean+alpha*st_dev) < 7.0:
        alpha += 0.5

    range1 = mini, mean-alpha*st_dev
    points =  mean-alpha*st_dev, mean+alpha*st_dev
    range4 =  mean+alpha*st_dev,maxi

    return range1,points,range4

def label_result(data,county_name, range1,points,range4):
    data['growth_label_estimate'] = ""
    for index, row in tqdm(data.iterrows()):
        i = row['daily_growth_range']


        if i > range4[1] :
            label = 'widespread'
            date = row['Date']
            df_index = (data['County Name'] == county_name) & (data['Date'] == date)
            data.loc[df_index,'growth_label_estimate'] = label
            #print(df_index,label)
            continue
        elif i >= range4[0] and i <= range4[1] :
            label = 'widespread'
            date = row['Date']
            df_index = (data['County Name'] == county_name) & (data['Date'] == date)
            data.loc[df_index,'growth_label_estimate'] = label
            #print(df_index,label)
            continue

        elif i <= points[1] and i >= points[0]:
            label = 'nochange'
            date = row['Date']
            df_index = (data['County Name'] == county_name) & (data['Date'] == date)
            data.loc[df_index,'growth_label_estimate'] = label
            #print(df_index,label)
            continue

        elif i <= range1[1] and i > range1[0] :
            label = 'minimal'
            date = row['Date']
            df_index = (data['County Name'] == county_name) & (data['Date'] == date)
            data.loc[df_index,'growth_label_estimate'] = label
            #print(df_index,label)
            continue
        elif i < range1[1] :
            label = 'minimal'
            date = row['Date']
            df_index = (data['County Name'] == county_name) & (data['Date'] == date)
            data.loc[df_index,'growth_label_estimate'] = label
            #print(df_index,label)
            continue

    return data