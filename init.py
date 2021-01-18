import sys
import csv
import subprocess
import pkg_resources
from os import path


# If directories.csv doesn't exist create it and add 'name,path'
# Next, check if requirements are satisfied
def main():
    if path.isfile('directories.csv') is True:
        pass
    else:
        with open('directories.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, escapechar=' ', quoting=csv.QUOTE_NONE)
            writer.writerow(['name', 'path'])
    # Check if requirements are satisfied
    try:
        dependencies = ['pandas', 'pyperclip']
        pkg_resources.require(dependencies)
    except:
        requirements()


# TODO: variable 'dependencies' should read off 'requirements.txt'
# Check if each requirment is satisfied, if not prompt user to install requirement
def requirements():
    dependencies = ['pandas', 'pyperclip==1.8.1']
    install_list = []
    install_prompt = []
    for item in dependencies:
        try:
            pkg_resources.require(item)
            # If requirement is already installed append value 0
            install_list.append([item, 0])
        except:
            # If requirement is NOT installed append value 1
            install_list.append([item, 1])
            install_prompt.append(item)
    check = sum(x[1] for x in install_list)
    if check > 0:
        while True:
            print('FastNav requires {prompt}'.format(prompt=install_prompt))
            answer = input('Install? (Y/N): ')
            answer = answer.upper()
            if answer == 'Y':
                for item in install_list:
                    if item[1] == 1:
                        requirement = item[0]
                        print('Installing', requirement, '(This may take awhile...)')
                        subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
                break
            if answer == 'N':
                print('Operation canceled')
                exit()
    else:
        pass


if __name__ == "__main__":
    main()