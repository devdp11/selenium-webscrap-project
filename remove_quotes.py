def remove_quotes_from_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = infile.read()

    data_no_quotes = data.replace('"', '')

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        outfile.write(data_no_quotes)

input_file = './assets/data.csv'
output_file = './assets/data_final.csv'
remove_quotes_from_csv(input_file, output_file)
