import os
import pandas as pd
import csv
import sys
import argparse
import pyperclip

import init
init.main()


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


# TODO: Add functionality to handel duplicate names/overwrites
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
def delete_d(del_d):
    df = pd.read_csv('directories.csv', index_col=0)
    try:
        # Prompt user if they want to delete directory
        prompt_msg = df.loc[del_d].values.tolist()
        prompt_msg.insert(0, del_d)
        while True:
            print(prompt_msg)
            check = input('Do you wish to remove? (Y/N): ')
            check = check.upper()
            if check == 'Y':
                df = df.drop(del_d)
                df.to_csv(r'directories.csv')
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

# # # # # # # # # # #
# End Of Functions  #
# # # # # # # # # # #


if __name__ == "__main__":
    # List commands if -ls flag is used
    if sys.argv[1] == '-ls':
        with open('directories.csv') as csv_file:
            directories = csv.reader(csv_file)
            next(csv_file)
            # If directories.csv is empty prompt user to add a new directory
            check = sum(1 for row in directories)
            if check == 0:
                print('Directories.csv is blank. Do \'fn -a\' to add directory')
                exit()
            for x, row in enumerate(directories, 1):
                print(x, row)
        exit()

    # If -a tag is used, prompt user to add a new directory and name
    if sys.argv[1] == '-a':
        a_parser = argparse.ArgumentParser(description='FastNav Variables')
        a_parser.add_argument('-a', '--add', type=str, nargs='+', help='Name of directory to delete')
        a_args = a_parser.parse_args()

        name = str_convert(a_args.add)
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
    parser.add_argument('name', type=str, metavar='', help='Name of the directory you\'d like to access')
    parser.add_argument('-o', '--open', type=int, nargs='?', const=1, help='Open directory in explorer window')
    args = parser.parse_args()

    # If -o tag is used, open directory in explorer window
    if args.open is not None:
        d_path(args.name)
        os.chdir(d__path)
        os.system('start .')
        exit()

    # If no tag is used, copy directory to clipboard
    d_path(args.name)
    pyperclip.copy(d__path)
    print('\'{arg}\' copied to clipboard'.format(arg=args.name))