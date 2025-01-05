import pandas as pd
from datetime import datetime, timedelta

# Функция для фильтрации транзакций за текущий месяц
def filter_current_month_transactions(transactions):
    now = datetime.now()
    start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (start_date + timedelta(days=32)).replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(seconds=1)
    return transactions[(transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= end_date)]

# Укажите правильный путь к вашему файлу
file_path = '../data/operations (1).xlsx'

# Читаем данные из Excel-файла
df = pd.read_excel(file_path)

# Преобразуем столбцы с датами в формат datetime
df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%Y-%m-%d %H:%M:%S')
df['Дата платежа'] = pd.to_datetime(df['Дата платежа'], format='%Y-%m-%d %H:%M:%S')

# Фильтруем транзакции за текущий месяц
current_month_transactions = filter_current_month_transactions(df)

# Проверяем, что есть данные
print(current_month_transactions.head())
