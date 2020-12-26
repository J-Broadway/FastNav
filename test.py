import os
import csv

# Searches for matching name in first column of directories.csv
name = input('Search a directory name: ')
with open('directories.csv') as csv_file:
    directories = csv.reader(csv_file)

    try:
        for row in directories:
            if name == row[0]:
                d_name = row[1]
                # If %USERNAME% variable is used, replace it with user login
                if d_name.find('%USERNAME%') > 0:
                    d_name = d_name.replace('%USERNAME%', os.getlogin())
                os.chdir(d_name)
                os.system('start .')
                exit()
        print(d_name)
    except NameError:
        print("Directory does not exist")