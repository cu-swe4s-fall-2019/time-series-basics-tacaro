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
        self._duphandle = -1
        # _duphandle indicates how duplicate values should be handled:
        # 0 indicates that the values will be summed (activity, bolus, meal)
        # 1 indicates that the values will be averaged (smbg, hr, cgm, basal)
        # open file, create a reader from csv.DictReader, read input times
        # and values
        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._duphandle = 0
        elif 'smbg' in data_csv or 'hr' in data_csv or 'cgm' in data_csv or \
             'basal' in data_csv:
            self._duphandle = 1
        elif self._duphandle == -1:
            print("Unsure how to average duplicate values!")
            sys.exit(1)

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
        output = []  # a list of datetime values
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                output.append(self._value[i])
        if (len(output) == 0):
            print("Key_time not found!")
            return -1

        return output
        # pass

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        # COME BACK TO THIS!
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
    time_lst = []
    vals = []
    num_times = len(obj._time)
    type = obj._duphandle
    for i in range(num_times):
        time = obj._time[i]
        bad = datetime.timedelta(minutes=time.minute % res,
                                 seconds=time.second)
        time -= bad
        if (bad >= datetime.timedelta(minutes=math.ceil(res/2))):
            time += datetime.timedelta(minutes=res)
        obj._time[i] = time

    if num_times > 0:
        time_lst.append(obj._time[0])
        sch = obj.linear_search_value(obj._time[0])  # search
        if type == 0:
            vals.append(sum(sch))  # summed
        elif type == 1:
            vals.append(sum(sch)/len(sch))  # averaged

    for i in range(1, num_times):  # check for duplicates
        if obj._time[i] == obj._time[i - 1]:
            continue
        else:
            time_lst.append(obj._time[i])
            sch = obj.linear_search_value(obj._time[i])
            if type == 0:
                vals.append(sum(sch))  # summed
            elif type == 1:
                vals.append(sum(sch)/len(sch))  # averaged
    output = zip(time_lst, vals)
    return output
    # pass


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    zip_a = []
    zip_b = []
    annot_a = []
    annot_b = []
    out = base_name+'.csv'
    if isfile(out):
        raise NameError("File with that name already exists!")
    if key_file not in annotation_list:
        raise ValueError("Key_file not found!")
    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                annot_a.append(annotation_list[i])
                zip_a.append(data_list[i])
            else:
                annot_b.append(annotation_list[i])
                zip_b.append(data_list[i])

    zipper = ['time', key_file] + annot_b
    with open(base_name+'.csv', mode='w') as output:
        wtr = csv.writer(output, delimiter=',')  # define a writer
        wtr.writerow(zipper)
        for (time, val) in zip_a[0]:
            old = []
            for data in zip_b:
                start_length = len(old)
                for (timex, valsx) in data:
                    if time == timex:
                        old.append(valsx)
                if len(old) == start_length:
                    old.append(0)
            wtr.writerow([time, val] + old)
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
    out = args.output_file
    sorter = args.sort_key
    # pull all the folders in the file
    # list the folders
    try:
        files_lst = [f for f in listdir(folder_path) if f.endswith('.csv')]
        # take folder name arg
    except (FileNotFoundError, NameError):
        print("File or Folder Not Found")
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []

    for file in files_lst:
        # print(ImportData(folder_path+file))
        # OLD  data_lst = data_lst.append(ImportData(folder_path+file))
        #print(file)
        data_lst.append(ImportData(folder_path + '/' + file))

    if (len(data_lst) == 0):
        print('Data not found')
        sys.exit(1)
    print(data_lst)

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    for instance in data_lst:
        data_5.append(roundTimeArray(instance, 5))
    data_15 = []  # a list with time rounded to 15min
    for instance in data_lst:
        data_15.append(roundTimeArray(instance, 15))

    # print to a csv file
    printer_5 = printArray(data_5, files_lst, out+'5', sorter)
    printer_15 = printArray(data_15, files_lst, out+'15', sorter)

    # printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    # printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
