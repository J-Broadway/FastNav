import csv

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
    append.writerow(['hey', 'there'])