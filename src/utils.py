import json
import pandas as pd
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def load_user_settings(file_path: str) -> dict:
    """
    Загружает настройки пользователя из JSON файла.

    Аргументы:
        file_path (str): Путь к файлу user_settings.json.

    Возвращает:
        dict: Словарь с настройками пользователя.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Загружает данные о транзакциях из Excel файла и преобразует даты в формат datetime.

    Аргументы:
        file_path (str): Путь к файлу operations.xlsx.

    Возвращает:
        pd.DataFrame: DataFrame с транзакциями.
    """
    transactions = pd.read_excel(file_path)
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], dayfirst=True)
    return transactions

def get_currency_rates(currencies: list) -> dict:
    """
    Получает курсы валют для указанных валют из API.

    Аргументы:
        currencies (list): Список валют.

    Возвращает:
        dict: Курсы валют.
    """
    rates = {}
    for currency in currencies:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{currency}')
        if response.status_code == 200:
            data = response.json()
            rates[currency] = data['rates']['RUB']
    return rates

def get_stock_prices(stocks: list) -> dict:
    """
    Получает цены на акции для указанных акций из API.

    Аргументы:
        stocks (list): Список акций.

    Возвращает:
        dict: Цены на акции.
    """
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('STOCK_API_URL')
    stock_prices = {}
    for stock in stocks:
        response = requests.get(f'{base_url}/time_series?symbol={stock}&interval=1min&apikey={api_key}')
        if response.status_code == 200:
            data = response.json()
            time_series = data.get('values', [])
            if time_series:
                latest_data = time_series[0]
                stock_prices[stock] = float(latest_data['open'])
    return stock_prices