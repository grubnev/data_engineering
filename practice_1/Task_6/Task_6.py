#https://tradestie.com/api/v1/apps/reddit?date=2022-04-03
import json

with open('reddit.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

html_output = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>JSON to HTML Table</title>
</head>
<body>
<table>
  <thead>
    <tr>
      <th>Ticker</th>
      <th>No. of Comments</th>
      <th>Sentiment</th>
      <th>Sentiment Score</th>
    </tr>
  </thead>
  <tbody>
"""

for item in data:
    html_output += f"""
    <tr>
      <td>{item['ticker']}</td>
      <td>{item['no_of_comments']}</td>
      <td>{item['sentiment']}</td>
      <td>{item['sentiment_score']}</td>
    </tr>
"""

html_output += """
  </tbody>
</table>

</body>
</html>
"""

with open('result_6.html', 'w', encoding='utf-8') as file:
    file.write(html_output)