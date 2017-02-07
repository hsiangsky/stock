import os
from datetime import datetime

FOLDER = '/data/original'

def string_to_time(string):
    year, month, day = string.split('/')
    return datetime(int(year) + 1911, int(month), int(day))

def is_same(row1, row2):
    if not len(row1) == len(row2):
        return False

    for index in range(len(row1)):
        if row1[index] != row2[index]:
            return False
    else:
        return True

def main():
    file_names = os.listdir(FOLDER)
    for file_name in file_names:
        if not file_name.endswith('.csv'):
            continue

        dict_rows = {}

        # Load and remove duplicates (use newer)
        with open('{}/{}'.format(FOLDER, file_name), 'rb') as file:
            print 'Processing '+FOLDER+'/'+file_name
            for line in file.readlines():
                dict_rows[line.split(',', 1)[0]] = line
        print 'Processing '+file_name
        # Sort by date
        rows = [row for date, row in sorted(
            dict_rows.items(), key=lambda x: string_to_time(x[0]))]

        print file_name+' sorted'

        with open('{}/{}'.format(FOLDER, file_name), 'wb') as file:
            file.writelines(rows)

if __name__ == '__main__':
    main()
