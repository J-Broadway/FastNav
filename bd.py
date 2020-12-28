import os
import csv
import sys
import argparse
import pyperclip
# Sets d__path to directory path from directory name
def d_path(name):
    global d__path
    with open ('directories.csv') as csv_file:
        directories = csv.reader(csv_file)
        # Search for matching name in first column of directories.csv
        for row in directories:
            if name == row[0]:
                d__path = row[1]
                # If %USERNAME% variable is used, replace it with user login
                if d__path.find('%USERNAME%') > 0:
                    d__path = d__path.replace('%USERNAME%', os.getlogin())
                # If %HOMEPATH% variable is used, replace it with homepath
                if d__path.find('%HOMEPATH%') > 0:
                    from pathlib import Path
                    d__path = d__path.replace('%HOMEPATH%', str(Path.home()))
        # Return error if directory is not found
        try:
            d__path
        except NameError:
            print('Directory name \'{this}\' does not exist'.format(this=args.name))
            exit()

# List commands if -ls flag is used
if sys.argv[1] == '-ls':
    with open('directories.csv') as csv_file:
        directories = csv.reader(csv_file)
        next(csv_file)
        for x, row in enumerate(directories, 1):
            print(x, row)
    exit()

# Create parser
parser = argparse.ArgumentParser(description='Better Directory Variables')
parser.add_argument('-ls', '--list', type=int, nargs='?', const=1, help='List Ranges')
parser.add_argument('name', type=str, metavar='', help='name of the directory you\'d like to access')
parser.add_argument('-o', '--open', type=int, nargs='?', const=1, help='Open directory in explorer window')
args = parser.parse_args()

# If -o tag is used, open directory in explorer window
if args.open is not None:
    d_path(args.name)
    os.chdir(d__path)
    os.system('start .')
    exit()

# If no tag is used, launch AHK script
d_path(args.name)
pyperclip.copy(d__path)
print('\'{arg}\' copied to clipboard'.format(arg=args.name))
