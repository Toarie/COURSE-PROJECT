import pandas as pd
import requests
import json
from datetime import datetime

def load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла.

    Возвращает:
        pd.DataFrame: DataFrame с транзакциями.
    """
    return pd.read_excel('data/operations.xlsx')

def get_currency_rates() -> list:
    """
    Получает курсы валют из API.

    Возвращает:
        list: Список курсов валют.
    """
    response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
    data = response.json()
    rates = [{"currency": currency, "rate": rate} for currency, rate in data['rates'].items()]
    return rates

def get_stock_prices() -> list:
    """
    Получает цены на акции из API.

    Возвращает:
        list: Список цен на акции.
    """
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = []
    for stock in stocks:
        response = requests.get(f'https://api.twelvedata.com/price?symbol={stock}&apikey=your_api_key')
        data = response.json()
        stock_prices.append({"stock": stock, "price": data['price']})
    return stock_prices
