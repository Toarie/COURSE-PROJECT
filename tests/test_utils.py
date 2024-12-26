import pytest
from src.utils import load_transactions, get_currency_rates, get_stock_prices

def test_load_transactions():
    transactions = load_transactions()
    assert not transactions.empty

def test_get_currency_rates():
    rates = get_currency_rates()
    assert isinstance(rates, list)
    assert len(rates) > 0

def test_get_stock_prices():
    prices = get_stock_prices()
    assert isinstance(prices, list)
    assert len(prices) > 0
