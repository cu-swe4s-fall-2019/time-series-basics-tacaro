import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []

        # open file, create a reader from csv.DictReader, and read input times
        # and values

        with open(data_csv, "r") as fhandle:
            reader = csv.DictReader(fhandle)
            for row in reader:
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError:
                    print("Can't parse this time properly!")
                    print(row['time'])

            if row['value'] == 'low':
                self.value.append(40)
            elif row['value'] == 'high':
                self.value.append(300)
            else:
                self._value.append(row['value'])
            fhandle.close()

        folder_path = args.folder_name
        files_lst = [f for f in listdir(folder_path)
                     if isfile(join(folder_path, f))]

        data_lst = []
        for files in files_lst:
            data_lst.append(ImportData(folder_path+files))

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

    # pull all the folders in the file
    # list the folders
    folder_path = './smallData/'
    files_lst = [f for f in listdir(folder_path)
                 if isfile(join(folder_path, f))]
    print(files_lst)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    # print to a csv file
    # printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    # printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
