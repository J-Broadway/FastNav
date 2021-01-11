import pandas as pd
import csv


# Adds new directory to directories.csv
def new_d(name, directory):
    # Add newline if there is no newline in file
    csv_file = open('test.csv', 'r')
    lines = csv_file.readlines()
    for line in lines:
        if line.find('\n') < 0:
            with open('test.csv', 'a', newline='') as csv_file:
                add_enter = csv.writer(csv_file)
                add_enter.writerow('')
    # If newline available append new directory to directories.csv
    with open('test.csv', 'a', newline='') as csv_file:
        append = csv.writer(csv_file)
        append.writerow([name, directory])


# Removes directory from directories.csv
def delete_d(del_d):
    df = pd.read_csv('test.csv', index_col=0)
    try:
        df = df.drop(del_d)
    except KeyError:
        print('\'{name}\' not found'.format(name=del_d))
        exit()
    df.to_csv(r'test.csv')
    print('\'{name}\' successfully removed'.format(name=del_d))

