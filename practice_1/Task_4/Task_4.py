import csv


def remove_phone_column(rows):
    return [row[:4] for row in rows]

def calculate_and_filter_salary(rows):
    salaries = [float(row[3].strip('₽')) for row in rows]
    average_salary = sum(salaries) / len(salaries)
    filtered_rows = [row for row in rows if float(row[3].strip('₽')) >= average_salary]
    return filtered_rows

def filter_by_age(rows):
    filtered_rows = [row for row in rows if row[2].isdigit() and int(row[2]) > 25 + 36 % 10]
    return filtered_rows

input_filename = 'text_4_var_36'
output_filename = 'result_4.txt'

with open('text_4_var_36', 'r', newline='', encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)  # Пропустить заголовок
    rows = [row for row in reader]

rows = remove_phone_column(rows)
rows = calculate_and_filter_salary(rows)
rows = filter_by_age(rows)

rows.sort(key=lambda row: int(row[0]))

with open('result_4.txt', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header[:4])
    writer.writerows(rows)