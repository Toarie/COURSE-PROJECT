import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from src.utils import load_transactions, get_currency_rates, get_stock_prices, load_user_settings
from src.views import home_page, get_greeting, get_cards_data, get_top_transactions, events_page, get_expenses, get_income

class TestFinancialFunctions(unittest.TestCase):

    @patch('src.utils.open', new_callable=MagicMock)
    def test_load_user_settings(self, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file
        mock_file.read.return_value = '{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]}'

        user_settings = load_user_settings('user_settings.json')
        self.assertEqual(user_settings, {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOG"]})

    @patch('src.utils.pd.read_excel')
    def test_load_transactions(self, mock_read_excel):
        mock_transactions = pd.DataFrame({
            'Дата операции': ['01-10-2023 12:00:00', '02-10-2023 12:00:00', '03-10-2023 12:00:00'],
            'Дата платежа': ['01-10-2023 12:00:00', '02-10-2023 12:00:00', '03-10-2023 12:00:00'],
            'Номер карты': ['1234', '1234', '5678'],
            'Сумма операции': [100, -50, 200],
            'Категория': ['Еда', 'Транспорт', 'Еда'],
            'Описание': ['Обед', 'Такси', 'Ужин']
        })
        mock_read_excel.return_value = mock_transactions

        transactions = load_transactions('operations.xlsx')
        self.assertFalse(transactions.empty)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transactions['Дата операции']))
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(transactions['Дата платежа']))

    @patch('src.utils.requests.get')
    def test_get_currency_rates(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'rates': {
                'USD': 1.0,
                'EUR': 0.9
            }
        }
        mock_get.return_value = mock_response

        rates = get_currency_rates(['USD', 'EUR'])
        self.assertEqual(rates, {'USD': 1.0, 'EUR': 0.9})

    @patch('src.utils.requests.get')
    @patch('src.utils.os.getenv')
    def test_get_stock_prices(self, mock_getenv, mock_get):
        mock_getenv.side_effect = lambda key: {
            'API_KEY': 'test_api_key',
            'STOCK_API_URL': 'https://test_api_url'
        }.get(key)

        mock_response = MagicMock()
        mock_response.json.return_value = {'price': 150.0}
        mock_get.return_value = mock_response

        prices = get_stock_prices(['AAPL'])
        self.assertEqual(prices, {'AAPL': 150.0})

    @patch('src.views.load_transactions')
    @patch('src.views.load_user_settings')
    @patch('src.views.get_currency_rates')
    @patch('src.views.get_stock_prices')
    def test_home_page(self, mock_get_stock_prices, mock_get_currency_rates, mock_load_user_settings, mock_load_transactions):
        # Мокируем данные
        mock_transactions = pd.DataFrame({
            'Дата операции': ['2023-10-01', '2023-10-02', '2023-10-03'],
            'Номер карты': ['1234', '1234', '5678'],
            'Сумма операции': [100, -50, 200],
            'Категория': ['Еда', 'Транспорт', 'Еда'],
            'Описание': ['Обед', 'Такси', 'Ужин']
        })
        mock_load_transactions.return_value = mock_transactions

        mock_user_settings = {
            'user_currencies': ['USD', 'EUR'],
            'user_stocks': ['AAPL', 'GOOG']
        }
        mock_load_user_settings.return_value = mock_user_settings

        mock_get_currency_rates.return_value = {'USD': 1.0, 'EUR': 0.9}
        mock_get_stock_prices.return_value = {'AAPL': 150.0, 'GOOG': 2800.0}

        # Вызываем функцию
        response = home_page('2023-10-03 12:00:00')

        # Проверяем результат
        self.assertIn('greeting', response)
        self.assertIn('cards', response)
        self.assertIn('top_transactions', response)
        self.assertIn('currency_rates', response)
        self.assertIn('stock_prices', response)

    def test_get_greeting(self):
        self.assertEqual(get_greeting(datetime(2023, 10, 3, 8, 0, 0)), "Доброе утро")
        self.assertEqual(get_greeting(datetime(2023, 10, 3, 15, 0, 0)), "Добрый день")
        self.assertEqual(get_greeting(datetime(2023, 10, 3, 20, 0, 0)), "Добрый вечер")
        self.assertEqual(get_greeting(datetime(2023, 10, 3, 23, 0, 0)), "Доброй ночи")

    def test_get_cards_data(self):
        transactions = pd.DataFrame({
            'Номер карты': ['1234', '1234', '5678'],
            'Сумма операции': [100, -50, 200]
        })
        cards_data = get_cards_data(transactions)
        self.assertEqual(len(cards_data), 2)
        self.assertEqual(cards_data[0]['last_digits'], '1234')
        self.assertEqual(cards_data[0]['total_spent'], 50.0)
        self.assertEqual(cards_data[0]['cashback'], 0.5)

    def test_get_top_transactions(self):
        transactions = pd.DataFrame({
            'Дата операции': ['2023-10-01', '2023-10-02', '2023-10-03'],
            'Сумма операции': [100, -50, 200],
            'Категория': ['Еда', 'Транспорт', 'Еда'],
            'Описание': ['Обед', 'Такси', 'Ужин']
        })
        top_transactions = get_top_transactions(transactions)
        self.assertEqual(len(top_transactions), 3)
        self.assertEqual(top_transactions[0]['Сумма операции'], 200)

    @patch('src.views.load_transactions')
    @patch('src.views.load_user_settings')
    @patch('src.views.get_currency_rates')
    @patch('src.views.get_stock_prices')
    def test_events_page(self, mock_get_stock_prices, mock_get_currency_rates, mock_load_user_settings, mock_load_transactions):
        # Мокируем данные
        mock_transactions = pd.DataFrame({
            'Дата операции': ['2023-10-01', '2023-10-02', '2023-10-03'],
            'Номер карты': ['1234', '1234', '5678'],
            'Сумма операции': [100, -50, 200],
            'Категория': ['Еда', 'Транспорт', 'Еда'],
            'Описание': ['Обед', 'Такси', 'Ужин']
        })
        mock_load_transactions.return_value = mock_transactions

        mock_user_settings = {
            'user_currencies': ['USD', 'EUR'],
            'user_stocks': ['AAPL', 'GOOG']
        }
        mock_load_user_settings.return_value = mock_user_settings

        mock_get_currency_rates.return_value = {'USD': 1.0, 'EUR': 0.9}
        mock_get_stock_prices.return_value = {'AAPL': 150.0, 'GOOG': 2800.0}

        # Вызываем функцию
        response = events_page('2023-10-03', 'M')

        # Проверяем результат
        self.assertIn('expenses', response)
        self.assertIn('income', response)
        self.assertIn('currency_rates', response)
        self.assertIn('stock_prices', response)

    def test_get_expenses(self):
        transactions = pd.DataFrame({
            'Сумма операции': [-50, -30, -20, -10, -5, -3, -2],
            'Категория': ['Еда', 'Транспорт', 'Еда', 'Еда', 'Еда', 'Еда', 'Еда']
        })
        expenses = get_expenses(transactions)
        self.assertEqual(expenses['total_amount'], -125)
        self.assertIn('Еда', expenses['main'])
        self.assertIn('Остальное', expenses['main'])

    def test_get_income(self):
        transactions = pd.DataFrame({
            'Сумма операции': [100, 200, 300],
            'Категория': ['Зарплата', 'Зарплата', 'Зарплата']
        })
        income = get_income(transactions)
        self.assertEqual(income['total_amount'], 600)
        self.assertIn('Зарплата', income['main'])

# Тесты с использованием pytest

def test_load_transactions():
    transactions = load_transactions('operations.xlsx')
    assert not transactions.empty

def test_get_currency_rates():
    user_settings = load_user_settings('user_settings.json')
    user_currencies = user_settings.get('user_currencies', [])
    rates = get_currency_rates(user_currencies)
    assert isinstance(rates, dict)
    assert len(rates) > 0

def test_get_stock_prices():
    user_settings = load_user_settings('user_settings.json')
    user_stocks = user_settings.get('user_stocks', [])
    prices = get_stock_prices(user_stocks)
    assert isinstance(prices, dict)
    assert len(prices) > 0

def test_home_page():
    date_str = '2023-01-31 12:00:00'
    response = home_page(date_str)
    assert 'greeting' in response
    assert 'cards' in response
    assert 'top_transactions' in response
    assert 'currency_rates' in response
    assert 'stock_prices' in response

def test_events_page():
    date_str = '2023-01-31'
    response = events_page(date_str)
    assert 'expenses' in response
    assert 'income' in response
    assert 'currency_rates' in response
    assert 'stock_prices' in response

if __name__ == '__main__':
    unittest.main()
