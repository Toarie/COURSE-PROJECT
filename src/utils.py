import json
import pandas as pd
from datetime import datetime
import requests
import os

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
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'])
    return transactions

def get_currency_rates(currencies: list) -> dict:
    """
    Получает курсы валют для указанных валют из API.

    Аргументы:
        currencies (list): Список валют.

    Возвращает:
        dict: Курсы валют.
    """
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    rates = {currency: data['rates'].get(currency, 1.0) for currency in currencies}
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
        response = requests.get(f'{base_url}/price?symbol={stock}&apikey={api_key}')
        data = response.json()
        stock_prices[stock] = data.get('price', 100.0)
    return stock_prices

# Пример использования
user_settings = load_user_settings('user_settings.json')
transactions = load_transactions('data/operations.xlsx')
currency_rates = get_currency_rates(user_settings['user_currencies'])
stock_prices = get_stock_prices(user_settings['user_stocks'])

# Вывод результатов
print("Transactions:")
print(transactions.head())
print("\nCurrency Rates:")
print(currency_rates)
print("\nStock Prices:")
print(stock_prices)
