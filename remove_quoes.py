import csv

def remove_quotes_from_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = [row for row in reader]

    rows_no_quotes = [[cell.replace('"', '') for cell in row] for row in rows]

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows_no_quotes)

input_file = './assets/data.csv'
output_file = './assets/data_final.csv'

remove_quotes_from_csv(input_file, output_file)