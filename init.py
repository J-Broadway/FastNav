import os
import sys
import csv
import subprocess
from os import path


# If directories.csv doesn't exist create it and add 'name,path'
# Next, install requirements.txt
def main():
    if path.isfile('directories.csv') is True:
        pass
    else:
        with open('directories.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, escapechar=' ', quoting=csv.QUOTE_NONE)
            writer.writerow(['name', 'path'])
        # Install requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


if __name__ == "__main__":
    main()
