import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import sys


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._file = data_csv
        # open file, create a reader from csv.DictReader, read input times
        # and values

        with open(data_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['time'] == ''):
                    continue
                time = (datetime.datetime.strptime(row['time'],
                        '%m/%d/%y %H:%M'))

                try:
                    if (row['value'] == 'low'):
                        print('converting low to 40')
                        row['value'] = 40  # low to 40
                    elif (row['value'] == 'high'):
                        print('converting high to 300')
                        row['value'] = 300  # high to 300

                    val = float(row['value'])
                    if (not math.isnan(val)):
                        self._value.append(val)
                        self._time.append(time)
                except ValueError:
                    print('Throwing out this value: ' + row['value'])

            # Reverse the data if we find that the last time is less than the\
            # first time!
            if len(self._time) > 0:  # if time isn't empty
                if (self._time[-1] < self._time[0]):
                    self._time.reverse()
                    self._value.reverse()

            csvfile.close()

    def linear_search_value(self, key_time):
        # return list of value(s) associated with key_time
        # if none, return -1 and error message

        pass

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        pass


def roundTimeArray(obj, res):
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    pass


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    pass


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import, combine,\
    and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file')

    parser.add_argument('--sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()
    folder_path = args.folder_name
    # pull all the folders in the file
    # list the folders
    try:
        files_lst = listdir(folder_path)  # take folder name arg
    except (FileNotFoundError, NameError):
        print("File or Folder Not Found")
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    for file in files_lst:
        # print(ImportData(folder_path+file))
        # OLD  data_lst = data_lst.append(ImportData(folder_path+file))
        data_lst.append(ImportData(folder_path + '/' + file))

    if (len(data_lst) == 0):
        print('Data not found')
        sys.exit(1)
    print(data_lst)

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    # print to a csv file
    # printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    # printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
