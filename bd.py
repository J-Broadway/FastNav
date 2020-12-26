import os
import csv
import argparse

notfound = "Directory does not exist"

# Create parser
parser = argparse.ArgumentParser(description='Better Directory Variables')
parser.add_argument('-ls', '--list', type=int, nargs='?', const=1, help='List Ranges')
parser.add_argument('name', type=str, metavar='', help='name of the directory you\'d like to access')
args = parser.parse_args()

if args.list is not None:
    with open('directories.csv') as csv_file:
        directories = csv.reader(csv_file)
        for row in directories:
            print(row)
    exit()
# Searches for matching name in first column of directories.csv
# name = input('Search a directory name: ')
with open('directories.csv') as csv_file:
    directories = csv.reader(csv_file)

    try:
        for row in directories:
            if args.name == row[0]:
                d_name = row[1]
                # If %USERNAME% variable is used, replace it with user login
                if d_name.find('%USERNAME%') > 0:
                    d_name = d_name.replace('%USERNAME%', os.getlogin())
                try:
                    os.chdir(d_name)
                    os.system('start .')
                except FileNotFoundError:
                    print(notfound)
                exit()
        print(d_name)
    except NameError:
        print(notfound)
