def calculate_sum(line):
    numbers = line.split(',')
    try:
        total_sum = sum(map(int, numbers))
        return total_sum
    except ValueError:
        return 0


with open('text_2_var_36', 'r') as infile, open('result_2.txt', 'w') as outfile:
    for line in infile:
        total_sum = calculate_sum(line)
        outfile.write(f"{total_sum}\n")