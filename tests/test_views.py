import pytest
from src.views import home_page, events_page

def test_home_page():
    date_str = '2023-10-01 12:00:00'
    response = home_page(date_str)
    assert "greeting" in response
    assert "cards" in response
    assert "top_transactions" in response
    assert "currency_rates" in response
    assert "stock_prices" in response

def test_events_page():
    date_str = '2023-10-01'
    response = events_page(date_str)
    assert "expenses" in response
    assert "income" in response
    assert "currency_rates" in response
    assert "stock_prices" in response
