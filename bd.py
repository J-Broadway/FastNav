import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='Better Directory Variables')
parser.add_argument('name', type=str, metavar='', help='name of the directory you\'d like to access')
args = parser.parse_args()

if args.name == "batch":
    directory = os.path.join('C:/', 'Users', os.getlogin(), 'Batch')
    os.chdir(directory)
    os.system('start .')

else:
    print("Directory not found")