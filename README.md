# time-series-basics

Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data.

Traivs CI: [![Build Status](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tacaro.svg?branch=master)](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-tacaro)

## Installation

This package requires Python3 and the following python packages:

- sys
- os
- csv
- datetime
- math
- argparse
- unittest
- pycodestyle

Pycodestyle is required to run the tests: `pip install pycodestyle` or `pip install --upgrade pycodestyle`

ssshtest is required to run functional tests `test -e ssshtest || wget -qhttps://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest . ssshtest`

## Usage

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
