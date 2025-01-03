import pandas as pd
import requests
import os

def load_transactions() -> pd.DataFrame:
    """
    Загружает транзакции из Excel-файла и преобразует даты в формат datetime.

    Возвращает:
        pd.DataFrame: DataFrame с транзакциями.
    """
    transactions = pd.read_excel('data/operations.xlsx')
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])
    transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'])
    return transactions

def get_currency_rates() -> list:
    """
    Получает курсы валют из API и переводит их в RUB.

    Возвращает:
        list: Список курсов валют.
    """
    response = requests.get('https://api.exchangerate-api.com/v4/latest/RUB')
    data = response.json()
    rates = [{"currency": currency, "rate": rate} for currency, rate in data['rates'].items()]
    return rates

def get_stock_prices() -> list:
    """
    Получает цены на акции из API.

    Возвращает:
        list: Список цен на акции.
    """
    api_key = os.getenv('API_KEY')
    base_url = os.getenv('STOCK_API_URL')
    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    stock_prices = []
    for stock in stocks:
        response = requests.get(f'{base_url}/price?symbol={stock}&apikey={api_key}')
        data = response.json()
        stock_prices.append({"stock": stock, "price": data['price']})
    return stock_prices
