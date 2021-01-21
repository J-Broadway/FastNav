import init
init.main()

import os
import pandas as pd
import csv
import sys
import subprocess
import argparse
import pyperclip


# Returns directory path from directory name
def d_path(name):
    with open('directories.csv') as csv_file:
        directories = csv.reader(csv_file)
        # Grab sub folders
        sub_folder = ''
        if name.find('/') > 0 and name != '/':
            sub_folder = name[name.find('/'):].replace('/', '\\')
            name = name[0:name.find('/')]
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
                return d__path + sub_folder
        # Return error if directory is not found
        print('Directory name \'{this}\' does not exist'.format(this=args.name))
        exit()


# Adds new directory to directories.csv
def new_d(name, directory):
    # Add newline if there is no newline in file
    csv_file = open('directories.csv', 'r')
    lines = csv_file.readlines()
    for line in lines:
        if line.find('\n') < 0:
            with open('directories.csv', 'a', newline='') as csv_file:
                add_enter = csv.writer(csv_file)
                add_enter.writerow('')
    # If newline available append new directory to directories.csv
    with open('directories.csv', 'a', newline='') as csv_file:
        append = csv.writer(csv_file)
        append.writerow([name, directory])


# Removes directory from directories.csv
def delete_d(del_d, mode=0):
    df = pd.read_csv('directories.csv', index_col=0)
    try:
        while True:
            check = ''
            # If mode is 0, prompt user if they want to delete directory
            if mode == 0:
                prompt_msg = df.loc[del_d].values.tolist()
                prompt_msg.insert(0, del_d)
                print(prompt_msg)
                check = input('Do you wish to remove? (Y/N): ')
                check = check.upper()
            # Otherwise is mode is 1, remove directory
            if mode == 1:
                check = 'Y'
            if check == 'Y':
                df = df.drop(del_d)
                df.to_csv(r'directories.csv')
                if mode == 0:
                    print('\'{name}\' successfully removed'.format(name=del_d))
                break
            if check == 'N':
                print('Operation canceled')
                break
    except KeyError:
        print('\'{name}\' not found'.format(name=del_d))
        exit()


# Converts list into a string
def str_convert(my_list):
    if len(my_list) > 1:
        # If list has more than 1 item, join as a string
        my_list = ' '.join(my_list)
    else:
        my_list = my_list[0]
    return my_list


# Checks if executable
def is_exe(exe_path):
    return os.path.isfile(exe_path) and os.access(exe_path, os.X_OK)


# # # # # # # # # # #
# End Of Functions  #
# # # # # # # # # # #


if __name__ == "__main__":
    # If no command is used return error
    if len(sys.argv) == 1:
        print('Error: No arguments. Do \'fn -h\' for help.')
        exit()
    # List commands if -ls flag is used
    if sys.argv[1] == '-ls':
        # If directories.csv is empty prompt user to add a new directory
        with open('directories.csv') as csv_file:
            directories = csv.reader(csv_file)
            next(csv_file)
            check = sum(1 for row in directories)
            if check == 0:
                print('Directories.csv is blank. Do \'fn -a\' to add directory')
                exit()
        # If directories.csv is not empty list directories
        with open('directories.csv') as csv_file:
            directories = csv.reader(csv_file)
            next(csv_file)
            for x, row in enumerate(directories, 1):
                print(x, row)
        exit()

    # If -a tag is used, prompt user to add a new directory and name
    if sys.argv[1] == '-a':
        a_parser = argparse.ArgumentParser(description='FastNav Variables')
        a_parser.add_argument('-a', '--add', type=str, nargs='+', help='Name of directory to add')
        a_args = a_parser.parse_args()
        name = str_convert(a_args.add)

        # Check name doesn't already exist
        df = pd.read_csv('directories.csv', index_col=0)
        exists = name in df.index
        if exists is True:
            print('Directory \'{name}\' already exists'.format(name=name))
            overwrite = input('Overwrite? (Y/N): ')
            overwrite = overwrite.upper()
            while True:
                if overwrite == 'Y':
                    delete_d(name, 1)
                    break
                if overwrite == 'N':
                    print('Operation Canceled')
                    exit()
        directory = input('Directory Path: ')
        while True:
            print('{name}, {directory}'.format(name=name, directory=directory))
            check = input('Is this correct? (Y/N): ')
            check = check.upper()
            if check == 'Y':
                new_d(name, directory)
                print('\'{name}\' added successfully'.format(name=name))
                break
            if check == 'N':
                print('Operation canceled')
                break
        exit()

    # If -rm tag is used, prompt user to delete directory
    if sys.argv[1] == '-rm':
        d_parser = argparse.ArgumentParser(description='FastNav Variables')
        d_parser.add_argument('-rm', '--remove', type=str, nargs='+', help='Name of directory to delete')
        d_args = d_parser.parse_args()

        delete_me = str_convert(d_args.remove)
        delete_d(delete_me)
        exit()

    # Create parser
    parser = argparse.ArgumentParser(description='FastNav Variables')
    parser.add_argument('-ls', '--list', type=int, nargs='?', const=1, help='List directories')
    parser.add_argument('-a', '--add', type=int, nargs='?', const=1, help='Add a new directory')
    parser.add_argument('name', type=str, metavar='', nargs='+', help='Name of the directory you\'d like to access')
    parser.add_argument('-c', '--copy', type=int, nargs='?', const=1, help='Copy directory to clipboard')
    args = parser.parse_args()
    # This will convert directory names with spaces (IE: 'my desktop') to a string instead of list
    name = str_convert(args.name)

    # If -c tag is used, copy directory to clipboard
    # Can you see me?
    if args.copy is not None:
        pyperclip.copy(d_path(name))
        print('\'{arg}\' copied to clipboard'.format(arg=name))
        exit()

    # If no tag is used, execute file, or open program in explorer window
    exec_check = is_exe(d_path(name))
    if exec_check is True:
        os.startfile(d_path(name), 'open')
    else:
        os.chdir(d_path(name))
        os.system('start .')
        exit()