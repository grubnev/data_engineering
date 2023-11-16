def calculate_sum(line):
    numbers = line.split(',')
    try:
        total_sum = sum(map(int, numbers))
        return total_sum
    except ValueError:
        return 0

input_filename = 'text_2_var_36'
output_filename = 'result_2.txt'

with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    for line in infile:
        total_sum = calculate_sum(line)
        outfile.write(f"{total_sum}\n")