import numpy as np

# Загрузка матрицы из файла в формате npy
matrix = np.load('matrix_36_2.npy')

# Определение условия для отбора значений
threshold_value = 500 + 36

# Отбор значений, которые превышают порог
indices_x, indices_y = np.where(matrix > threshold_value)
values_z = matrix[indices_x, indices_y]

# Сохранение массива в файле формата npz
np.savez('output_arrays.npz', x=indices_x, y=indices_y, z=values_z)

# Сохранение массива в сжатом виде с использованием np.savez_compressed()
np.savez_compressed('output_arrays_compressed.npz', x=indices_x, y=indices_y, z=values_z)

# Сравнение размеров файлов
import os
size_regular = os.path.getsize('output_arrays.npz')
size_compressed = os.path.getsize('output_arrays_compressed.npz')

print(f"Размер файла без сжатия: {size_regular} байт")
print(f"Размер файла с сжатием: {size_compressed} байт")