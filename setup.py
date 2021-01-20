from sys import stdout
from os import getcwd

def main():
    cwd = getcwd()
    with open(r'temp\fn_temp.txt', 'r') as f:
        path_vars = f.read()
        if path_vars.find(cwd) != -1:
            stdout.write('0')
        else:
            stdout.write('1')


if __name__ == '__main__':
    main()