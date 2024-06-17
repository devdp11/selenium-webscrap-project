import csv

input_file = './assets/data.csv'
output_file = './assets/data_final.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    
    new_header = header[:1] + ['result'] + header[1:]
    
    rows = []
    
    for row in reader:
        new_row = row[:1] + [''] + row[1:]
        rows.append(new_row)

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(new_header)
    writer.writerows(rows)