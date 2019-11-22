import csv
import sys

try:
    csv_file = sys.argv[1]
except IOError:
    print("No csv file specified.")
    sys.exit(1)
try:
    sub_name = sys.argv[2]
except IOError:
    print("No subject name specified.")
    sys.exit(1)

# return each line of csv file as list of strings
# concatenate those lists into list
rows = []
with open(csv_file, 'rt') as f:
    csv_reader = csv.reader(f)
    for line in csv_reader:
        rows.add(line)
print(rows)
print('test')
