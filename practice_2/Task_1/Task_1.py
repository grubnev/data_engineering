import numpy as np
import json

# Загрузка матрицы из файла
matrix = np.load('matrix_36.npy')

# Подсчет суммы и среднего арифметического всех элементов
total_sum = np.sum(matrix)
total_avg = np.mean(matrix)

# Подсчет суммы и среднего арифметического главной диагонали
main_diag_sum = np.trace(matrix)
main_diag_avg = np.mean(np.diagonal(matrix))

# Подсчет суммы и среднего арифметического побочной диагонали
secondary_diag_sum = np.trace(np.flip(matrix, axis=1))
secondary_diag_avg = np.mean(np.diagonal(np.flip(matrix, axis=1)))

# Нахождение максимального и минимального значения
max_value = np.max(matrix)
min_value = np.min(matrix)

# Запись результатов в JSON
result_json = {
    'sum': float(total_sum),
    'avr': float(total_avg),
    'sumMD': float(main_diag_sum),
    'avrMD': float(main_diag_avg),
    'sumSD': float(secondary_diag_sum),
    'avrSD': float(secondary_diag_avg),
    'max': float(max_value),
    'min': float(min_value)
}

# Сохранение JSON в файл
with open('Task_1_output.json', 'w') as json_file:
    json.dump(result_json, json_file)

# Нормализация и сохранение матрицы в формате npy
normalized_matrix = (matrix - np.min(matrix)) / (np.max(matrix) - np.min(matrix))
np.save('Task_1_norm_matrix.npy', normalized_matrix)