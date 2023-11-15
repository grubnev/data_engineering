from bs4 import BeautifulSoup

def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ""
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'lxml')

        item = dict()
        item['name'] = star.find_all("name")[0].get_text().strip()
        item['constellation'] = star.find_all("constellation")[0].get_text().strip()
        item['spectral-class'] = star.find_all("spectral-class")[0].get_text().strip()


        print(item['spectral-class'])

        return item

handle_file("zip_var_36(3)/1.xml")