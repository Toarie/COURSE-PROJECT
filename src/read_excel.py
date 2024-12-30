import pandas as pd

# Укажите правильный путь к вашему файлу
file_path = '../data/operations (1).xlsx'

# Читаем данные из Excel-файла
df = pd.read_excel(file_path)

# Проверяем, что есть данные
print(df.head())
