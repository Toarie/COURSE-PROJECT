import json
import pandas as pd
from datetime import datetime
from django.http import JsonResponse
from src.utils import load_transactions, get_currency_rates, get_stock_prices, load_user_settings

def home_page(date_str: str) -> JsonResponse:
    """
    Генерирует JSON-ответ для главной страницы.

    Аргументы:
        date_str (str): Дата и время в формате 'YYYY-MM-DD HH:MM:SS'.

    Возвращает:
        JsonResponse: JSON-ответ.
    """
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    transactions = load_transactions('operations.xlsx')

    # Преобразуем столбец 'Дата операции' в datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

    # Фильтруем транзакции за текущий месяц
    start_date = date.replace(day=1, hour=0, minute=0, second=0)
    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= date)]

    # Приветствие
    greeting = get_greeting(date)

    # Данные по картам
    cards_data = get_cards_data(filtered_transactions)

    # Топ-5 транзакций
    top_transactions = get_top_transactions(filtered_transactions)

    # Курсы валют
    user_settings = load_user_settings('user_settings.json')
    user_currencies = user_settings.get('user_currencies', [])
    currency_rates = get_currency_rates(user_currencies)

    # Цены на акции
    user_stocks = user_settings.get('user_stocks', [])
    stock_prices = get_stock_prices(user_stocks)

    response = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return JsonResponse(response, ensure_ascii=False, safe=False, json_dumps_params={'indent': 4})

def get_greeting(date: datetime) -> str:
    """
    Генерирует приветствие на основе текущего времени.

    Аргументы:
        date (datetime): Текущая дата и время.

    Возвращает:
        str: Приветственное сообщение.
    """
    hour = date.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"

def get_cards_data(transactions: pd.DataFrame) -> list:
    """
    Генерирует данные по каждой карте.

    Аргументы:
        transactions (pd.DataFrame): DataFrame с транзакциями.

    Возвращает:
        list: Список данных по картам.
    """
    cards = transactions['Номер карты'].unique()
    cards_data = []
    for card in cards:
        card_transactions = transactions[transactions['Номер карты'] == card]
        total_spent = card_transactions['Сумма операции'].sum()
        cashback = total_spent * 0.01
        cards_data.append({
            "last_digits": card,
            "total_spent": float(total_spent),
            "cashback": float(cashback)
        })
    return cards_data

def get_top_transactions(transactions: pd.DataFrame) -> list:
    """
    Получает топ-5 транзакций по сумме.

    Аргументы:
        transactions (pd.DataFrame): DataFrame с транзакциями.

    Возвращает:
        list: Список топ-транзакций.
    """
    top_transactions = transactions.nlargest(5, 'Сумма операции')
    return top_transactions[['Дата операции', 'Сумма операции', 'Категория', 'Описание']].to_dict(orient='records')

def events_page(date_str: str, period: str = 'M') -> JsonResponse:
    """
    Генерирует JSON-ответ для страницы событий.

    Аргументы:
        date_str (str): Дата в формате 'YYYY-MM-DD HH:MM:SS'.
        period (str): Период для фильтрации данных ('W', 'M', 'Y', 'ALL').

    Возвращает:
        JsonResponse: JSON-ответ.
    """
    date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    transactions = load_transactions('operations.xlsx')

    # Преобразуем столбец 'Дата операции' в datetime
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'])

    # Фильтруем транзакции на основе периода
    if period == 'W':
        start_date = date - pd.Timedelta(days=date.weekday())
    elif period == 'M':
        start_date = date.replace(day=1, hour=0, minute=0, second=0)
    elif period == 'Y':
        start_date = date.replace(month=1, day=1, hour=0, minute=0, second=0)
    elif period == 'ALL':
        start_date = transactions['Дата операции'].min()
    else:
        start_date = date.replace(day=1, hour=0, minute=0, second=0)

    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= date)]

    # Расходы
    expenses = get_expenses(filtered_transactions)

    # Доходы
    income = get_income(filtered_transactions)

    # Курсы валют
    user_settings = load_user_settings('user_settings.json')
    user_currencies = user_settings.get('user_currencies', [])
    currency_rates = get_currency_rates(user_currencies)

    # Цены на акции
    user_stocks = user_settings.get('user_stocks', [])
    stock_prices = get_stock_prices(user_stocks)

    response = {
        "expenses": expenses,
        "income": income,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return JsonResponse(response, ensure_ascii=False, safe=False, json_dumps_params={'indent': 4})

def get_expenses(transactions: pd.DataFrame) -> dict:
    """
    Получает данные о расходах.

    Аргументы:
        transactions (pd.DataFrame): DataFrame с транзакциями.

    Возвращает:
        dict: Данные о расходах.
    """
    expenses = transactions[transactions['Сумма операции'] < 0]
    total_amount = expenses['Сумма операции'].sum()
    main_categories = expenses.groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False).head(7)
    other_categories = expenses.groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False).iloc[7:].sum()
    main_categories['Остальное'] = other_categories
    transfers_and_cash = expenses[expenses['Категория'].isin(['Наличные', 'Переводы'])].groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False)

    return {
        "total_amount": total_amount,
        "main": main_categories.to_dict(),
        "transfers_and_cash": transfers_and_cash.to_dict()
    }

def get_income(transactions: pd.DataFrame) -> dict:
    """
    Получает данные о доходах.

    Аргументы:
        transactions (pd.DataFrame): DataFrame с транзакциями.

    Возвращает:
        dict: Данные о доходах.
    """
    income = transactions[transactions['Сумма операции'] > 0]
    total_amount = income['Сумма операции'].sum()
    main_categories = income.groupby('Категория')['Сумма операции'].sum().sort_values(ascending=False)

    return {
        "total_amount": total_amount,
        "main": main_categories.to_dict()
    }

