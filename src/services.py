import json
import pandas as pd
from datetime import datetime

def profitable_cashback_categories(data: pd.DataFrame, year: int, month: int) -> str:
    """
    Анализирует наиболее выгодные категории для кешбэка.

    Аргументы:
        data (pd.DataFrame): DataFrame с транзакциями.
        year (int): Год для анализа.
        month (int): Месяц для анализа.

    Возвращает:
        str: JSON-ответ с анализом кешбэка.
    """
    start_date = datetime(year, month, 1)
    end_date = (start_date + pd.DateOffset(months=1)) - pd.Timedelta(days=1)
    filtered_transactions = data[(data['Дата операции'] >= start_date) & (data['Дата операции'] <= end_date)]

    cashback_analysis = filtered_transactions.groupby('Категория')['Сумма операции'].sum() * 0.01
    cashback_analysis = cashback_analysis.to_dict()

    return json.dumps(cashback_analysis, ensure_ascii=False, indent=4)
