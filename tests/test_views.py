import unittest
from datetime import datetime
from src.views import home_page, events_page
import json

class TestViews(unittest.TestCase):
    def test_home_page(self):
        date_str = '2023-10-10 12:00:00'
        response = home_page(date_str)
        data = json.loads(response)
        self.assertIn('greeting', data)
        self.assertIn('cards', data)
        self.assertIn('top_transactions', data)
        self.assertIn('currency_rates', data)
        self.assertIn('stock_prices', data)

    def test_events_page(self):
        date_str = '2023-10-10'
        response = events_page(date_str, period='M')
        data = json.loads(response)
        self.assertIn('expenses', data)
        self.assertIn('income', data)
        self.assertIn('currency_rates', data)
        self.assertIn('stock_prices', data)

if __name__ == '__main__':
    unittest.main()