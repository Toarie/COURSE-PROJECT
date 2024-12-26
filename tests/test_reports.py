import pytest
from src.reports import spending_by_category
import pandas as pd

def test_spending_by_category():
    data = pd.DataFrame({
        'Дата операции': ['2023-10-01', '2023-10-02'],
        'Категория': ['Продукты', 'Продукты'],
        'Сумма операции': [1000, 2000]
    })
    response = spending_by_category(data, 'Продукты', '2023-10-02')
    assert isinstance(response, str)
    assert 'category' in response
    assert 'spending' in response
