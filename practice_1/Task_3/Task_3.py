import math

def replace_na_with_mean(numbers):
    for i in range(len(numbers)):
        if numbers[i] == "NA":
            left_idx = i - 1
            right_idx = i + 1

            while left_idx >= 0 and numbers[left_idx] == "NA":
                left_idx -= 1

            while right_idx < len(numbers) and numbers[right_idx] == "NA":
                right_idx += 1

            if left_idx >= 0 and right_idx < len(numbers):
                left_num = float(numbers[left_idx])
                right_num = float(numbers[right_idx])
                mean = (left_num + right_num) / 2
                numbers[i] = str(mean)
            elif left_idx >= 0:
                numbers[i] = numbers[left_idx]
            elif right_idx < len(numbers):
                numbers[i] = numbers[right_idx]


with open('text_3_var_36', 'r') as infile, open('result_3.txt', 'w') as outfile:
    for line in infile:
        numbers = line.strip().split(',')

        replace_na_with_mean(numbers)

        filtered_numbers = [num for num in numbers if math.sqrt(float(num)) >= (50 + 36)]

        outfile.write(",".join(filtered_numbers) + "\n")