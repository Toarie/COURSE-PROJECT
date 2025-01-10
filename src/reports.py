import json
import pandas as pd
from datetime import datetime
from functools import wraps

def report_decorator(file_name=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if file_name:
                with open(file_name, 'w') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
            else:
                with open('report_output.json', 'w') as f:
                    json.dump(result, f, ensure_ascii=False, indent=4)
            return result
        return wrapper
    return decorator

@report_decorator(file_name='spending_by_category_report.json')
def spending_by_category(transactions: pd.DataFrame, category: str, date: str = None) -> str:
    """
    Получает траты по категории за последние три месяца.

    Аргументы:
        transactions (pd.DataFrame): DataFrame с транзакциями.
        category (str): Название категории.
        date (str): Опциональная дата в формате 'YYYY-MM-DD'.

    Возвращает:
        str: JSON-ответ с тратами по категории.
    """
    if date:
        end_date = datetime.strptime(date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    start_date = end_date - pd.DateOffset(months=3)
    filtered_transactions = transactions[(transactions['Дата операции'] >= start_date) & (transactions['Дата операции'] <= end_date)]

    category_spending = filtered_transactions[filtered_transactions['Категория'] == category]['Сумма операции'].sum()

    return json.dumps({"category": category, "spending": float(category_spending)}, ensure_ascii=False, indent=4)