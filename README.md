# time-series-basics

Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data.

Traivs CI: [![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tacaro.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tacaro)

## Files:
- data_import.py: Legacy python script for importing time series data.
- pandas_import.py: Newly updated script that utilizes pandas for importing, cleaning, and printing time series data.
- big_df5.csv: 5 minute-rounded output from pandas_import.py
- big_df15.csv 15 minute-rounded output from pandas_import.py

## Installation

This package requires Python3 and the following python packages:

- sys
- pandas
- numpy
- os
- csv
- datetime
- math
- argparse
- unittest
- pycodestyle

Pycodestyle is required to run the tests: `pip install pycodestyle` or `pip install --upgrade pycodestyle`

ssshtest is required to run functional tests `test -e ssshtest || wget -qhttps://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest . ssshtest`

## Usage [pandas_import.py]
The new pandas_import is based on the pandas python package.
1. Import csv files using `pd.readcsv('/SmallData/filename.csv')`
2. Create parallel arrays of the files themselves and the file names, as pulled from the directory with `os.path.splitext(x)[0]` so as to strip the '.csv' extensions.
3. Convert time columns to datetime type, convert value column to numeric, and change value column name to correspond to the file it was pulled from:
```
for k in range(len(all_files)):
      # print(k)
      file = all_files[k]
      file['time'] = pd.to_datetime(file['time'])
      file.apply(lambda x: pd.to_numeric(x, errors='coerce')).dropna()
      file.rename(columns={'value': dirlst[k]}, inplace=True)
```
4. Left-join the data frames using cgm_small as the anchor-point. This is done with a short loop:
```
big_df = cgm_small.merge(all_files[0], on='time', how='left')
  for incoming_df in all_files[1:]:
      big_df = big_df.merge(incoming_df, on='time', how='left')
```
5. NaNs are replaced with zero using `.fillna(value=0, inplace=True)`

6. .groupby() in conjunction with .sum() are used to produce new dataframes with the columns summed and grouped by the specified characteristics.

7. .rename() is used to tidy up the column names.

8. New csvs are saved with `.tocsv()`

## Benchmarking
Using GNU-Time, the pandas_import.py script took 5.83 seconds and used 74472kb of memory.

Similarly, the data_import.py script took 31.46 seconds and used 444091kb of memory.

## Usage [Legacy]

data_import.py is the executed script. It is used in the following manner: `python data_import.py --folder_name smallData --output_file out --sort_key hr_small.csv` where --folder_name is the folder containing .csv files, --output_file is the name of the desired output .csv file --sort_key is the file used to sort the data

### ImportData

ImportData is the major class of data_import.py It takes a.csv file that contains time and value columns.

- time: an array containing datetime objects
- value: a parallel array containing values
- file: the filename

**Functions:**

- linear_search_value: returns the values of a given datetime object. Returns -1 if no values match.

## roundTimeArray

Takes in 'obj', an ImportData instance, and 'res', the resolution for rounding. It creates a list of datetime objects and values that are rounded to 'res', ensures no duplicate times, and handles duplicates in a pre-defined manner. roundTimeArray outputs an iterable zip object that contains time,value arrays.

## printArray

Creates a csv that is aligned to the key_file. Creates a csv titled base_name.csv.
