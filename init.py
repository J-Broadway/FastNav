from os import path
import csv


# If directories.csv doesn't exist create it and add 'name,path'
def main():
    if path.isfile('directories.csv') is True:
        pass
    else:
        with open('directories.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, escapechar=' ', quoting=csv.QUOTE_NONE)
            writer.writerow(['name', 'path'])


if __name__ == "__main__":
    main()
