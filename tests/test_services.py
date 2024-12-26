import pytest
from src.services import profitable_cashback_categories
import pandas as pd

def test_profitable_cashback_categories():
    data = pd.DataFrame({
        'Дата операции': ['2023-10-01', '2023-10-02'],
        'Категория': ['Продукты', 'Рестораны'],
        'Сумма операции': [1000, 2000]
    })
    response = profitable_cashback_categories(data, 2023, 10)
    assert isinstance(response, str)
    assert 'Продукты' in response
    assert 'Рестораны' in response
