# Time Series

- Combining data from multiple files
- Align a key (time stamp)
- Print to CSV
- `datetime`

## Reading Multiple CSVs from a folder

If we want to specify just the folder name and import all the files from inside said folder:

1. Specify Folder Name
2. Use `listdir()` to list all items in the folder If the item is a file (not a folder), as tested with `isfile()`.

  ```
  folder_path = './DataFiles/'
  files = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
  ```

We can use the CSV module to read csv files the same way we use `open()` to read text files.

```
import csv
with open('myFile.csv') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
    print(row['Column1'], row['Column2'])

1 2
3 4
```

This is pretty slick. Unlike in open(), which requires us to strip invisible characters, we can just pull data from a column.

We can make this process easier by creating a class that imports data and places it into lists using `append()`. See below code for example.

## Datetime Module

Python's datetime allows us to parse dates and times using oBjEcT oRiEnTeD PrOgRaMmInG

1. Convert string date/timie into a datetime object with the `dateutil.parser` module.
2. Use the `parse()` function from this module to convert the string to a datetime object.

```
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
            self._value.append(row['value'])
            fhandle.close()
```

## Combining Multiple Files

Since we have an import data class, we can add a function to our main method that instantiates objects from each file we want to import. Continued from above:

```
if __name__ == '__main__':
      parser = argparse.ArgumentParser(
          description='Folder Name For Data To Import',
          prog='dataImport')

      parser.add_argument('folder_name',
                          type=str,
                          help='Name Of Folder',
                          required=True)

      args = parser.parse_args()

      folder_path = args.folder_name
      files_lst = [f for f in listdir(folder_path)
                   if isfile(join(folder_path, f))]

      data_lst = []
      for files in files_lst:
          data_lst.append(ImportData(folder_path+files))
```

### Fun with Lists!

- list.append(x) adds x to the end of the list
- list.extend(iterable) appends all the items from the iterable to the list
- list.insert(i,x) inserts item x at position i
- list.remove(x) Remove the first instance of x within a list
- list.pop([i]) Remove the item at [optional] position i in the list and return it. If no position is supplied, the last item in the list is removed and returned.
- list.clear() Removes all items from the list
- list.count(x) Counts the number of times x appears in the list.
- list.reverse() Reverse the elements of a list in place
- len(list) Returns the length of a list

**List Membership** We can check if an element is in a list with "in" and "not in" Returns True or False.

**List of Lists** The operator for "x" in "y" can iterate through a list of lists.

```
for (gene, values) in gene_data:
  print(gene, values)
```

**List Ops** Addition concatenates lists. Multiplication replicates the list.

```
A = [1,2,3]
B = [100, 200, 300]
C = A+B
C
--> [1,2,3,100,200,300]
A*3
--> [1,2,3,1,2,3,1,2,3]
```

**List Slicing** Colon indicates "the rest of the values" A[3:] returns index 3 to the end of the list. Start value is inclusive, stop value is exclusive.

### Mapping Parallel Arrays [Iterables] Together

We can associate multiple values together with `zip()`

```
names = [gene1, gene2, gene3]
values = [4,5,6]
gene_values = zip(names, values)
gene_values
--> <zip object at 0x10fc740c8>
```

So we need to cast the zip object as a list `list(gene_values)`

We can unzip the iterable using zip( * )

```
unzip_names, unzip_values = zip(*gene_values)
```

This is pretty slick, as we can use zip to iterate through pairs of elements:

```
for nam, val in gene_values:
  print('Gene '+str(nam)+' has value '+str(val))
```

#### Printing to CSV

Writing to a CSV requires creating an opened file object using open() and writing with the write() function. We need two things:

1. Write out strings
2. End each line with a newline command `\n`

```
file = open('newfile.csv', 'w')
file.write('Gene Name, Value \n') # column header

for nam, val in gene_values:
  file.write(str(nam)+', '+str(val)+'\n') # comma separated name/value pairs
```
