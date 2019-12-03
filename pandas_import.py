import numpy as np
import pandas as pd
import datetime as dt
import os
import math

if __name__ == "__main__":
    activity_small = pd.read_csv("smallData/activity_small.csv")
    basal_small = pd.read_csv("smallData/basal_small.csv")
    bolus_small = pd.read_csv("smallData/bolus_small.csv")
    cgm_small = pd.read_csv("smallData/cgm_small.csv")
    hr_small = pd.read_csv("smallData/hr_small.csv")
    meal_small = pd.read_csv("smallData/meal_small.csv")
    smbg_small = pd.read_csv("smallData/smbg_small.csv")
    all_files = [activity_small, basal_small, bolus_small, cgm_small, hr_small,
                 meal_small, smbg_small]
    dirlst = sorted([os.path.splitext(x)[0] for x in os.listdir('smallData')])
    # all_files and dirlst are parallel arrays

    '''
    1. Convert time to datetime type
    2. Convert value column to numeric
    3. change value column name to correspond to file name
    '''
    for k in range(len(all_files)):
        # print(k)
        file = all_files[k]
        file['time'] = pd.to_datetime(file['time'])
        file.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
        file.rename(columns={'value': dirlst[k]}, inplace=True)

    '''Left-join the dfs using cgm_small as the main df.
    Pass the list of other dfs to the join function.'''
    # https://stackoverflow.com/questions/53645882/pandas-merging-101
    big_df = cgm_small.merge(all_files[0], on='time', how='left')
    for incoming_df in all_files[1:]:
        big_df = big_df.merge(incoming_df, on='time', how='left')

    '''Replace NaNs with 0'''
    big_df.fillna(value=0, inplace=True)

    '''Using datetime.dt.round() add time5 column and time15 column where the
    values are index values rounded to nearest 5 and 15 min'''
    big_df['time5'] = big_df['time'].dt.round('5min')
    big_df['time15'] = big_df['time'].dt.round('15min')
    # print(big_df.info())

    '''Use the groupby() function on your rounded time columns to construct
    two new data structures, one with indexes being the 5 min and the other
    with 15min inettvals. Include only the data columns in these new dfs
    Handle data as follows:
    Activity, bolus, meal: sum the values
    Smbg, hr, cgm, basal: average the values
    '''
    # Group by rounding, generate sums and means
    big_df5_sum = pd.DataFrame(big_df.groupby('time5').sum())
    big_df5_avg = pd.DataFrame(big_df.groupby('time5').mean())
    big_df15_sum = pd.DataFrame(big_df.groupby('time15').sum())
    big_df15_avg = pd.DataFrame(big_df.groupby('time15').mean())

    # Replacing the sums with avgs
    big_df5_out = big_df5_sum
    big_df5_out['smbg_small'] = big_df5_avg['smbg_small']
    big_df5_out['hr_small'] = big_df5_avg['hr_small']
    big_df5_out['cgm_small_x'] = big_df5_avg['cgm_small_x']
    big_df5_out['basal_small'] = big_df5_avg['basal_small']

    big_df15_out = big_df15_sum
    big_df15_out['smbg_small'] = big_df15_avg['smbg_small']
    big_df15_out['hr_small'] = big_df15_avg['hr_small']
    big_df15_out['cgm_small_x'] = big_df15_avg['cgm_small_x']
    big_df15_out['basal_small'] = big_df15_avg['basal_small']

    big_df5_out.rename(columns={'smbg_small': 'smbg', 'cgm_small_x': 'cgm',
                                'basal_small': 'basal', 'bolus_small': 'bolus',
                                'hr_small': 'hr', 'meal_small': 'meal',
                                'smbg_small': 'smbg'}, inplace=True)

    big_df15_out.rename(columns={'smbg_small': 'smbg', 'cgm_small_x': 'cgm',
                                 'basal_small': 'basal',
                                 'bolus_small': 'bolus',
                                 'hr_small': 'hr', 'meal_small': 'meal',
                                 'smbg_small': 'smbg'}, inplace=True)

    '''Save df as csv'''
    big_df5_out.to_csv('big_df5.csv')
    big_df15_out.to_csv('big_df15.csv')
