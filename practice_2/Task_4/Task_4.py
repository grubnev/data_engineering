import pandas as pd
import json

# Загрузка данных из файла формата pkl
with open('products_36.pkl', 'rb') as f:
    products_data = pd.read_pickle(f)

# Загрузка данных из файла формата json
with open('price_info_36.json', 'r') as f:
    prices_update_data = json.load(f)

# Обновление цен в соответствии с методами
for update in prices_update_data:
    product_name = update['name']
    method = update['method']
    param = update['param']

    # Находим соответствующий товар в списке
    for product in products_data:
        if product['name'] == product_name:
            if method == 'add':
                product['price'] += param
            elif method == 'sub':
                product['price'] -= param
            elif method == 'percent+':
                product['price'] *= (1 + param)
            elif method == 'percent-':
                product['price'] *= (1 - param)
            break  # Stop searching once the product is found and updated

# Сохранение модифицированных данных обратно в формат pkl
with open('modified_data.pkl', 'wb') as f:
    pd.to_pickle(products_data, f)