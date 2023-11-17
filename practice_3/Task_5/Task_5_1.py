from bs4 import BeautifulSoup
import numpy as np
import re
import json

def handle_file(file_name):

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()
        item['title'] = site.find_all('h1')[0].get_text()
        item['price'] = int(site.find_all('span', attrs={"itemprop": "price"})[0].get_text())

        props = site.find_all('div', attrs={"class":"col"})
        for prop in props:
            item[prop['type']] = prop.get_text().strip()

        items.append(item)

        print(item)

items = []
handle_file('1/1.html')