from bs4 import BeautifulSoup
import csv

with open('text_5_var_36', 'r', encoding='utf-8') as html_file:
    html = html_file.read()

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table')
data = []

headers = [header.get_text() for header in table.find_all('th')]
data.append(headers)

for row in table.find_all('tr'):
    cols = row.find_all('td')
    cols = [col.get_text().strip() for col in cols]
    data.append(cols)

with open('result_5.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data)