import unittest
from src.read_excel import filter_current_month_transactions
import pandas as pd
from datetime import datetime

class TestTransactionFiltering(unittest.TestCase):
    def test_filter_current_month_transactions(self):
        # Создаем тестовый DataFrame
        data = {
            'Дата операции': [
                '2023-10-15 12:34:56',
                '2023-11-01 00:00:00',
                '2023-11-15 12:34:56',
                '2023-12-01 00:00:00'
            ],
            'Дата платежа': [
                '2023-10-16 12:34:56',
                '2023-11-02 00:00:00',
                '2023-11-16 12:34:56',
                '2023-12-02 00:00:00'
            ]
        }
        transactions = pd.DataFrame(data)
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], format='%Y-%m-%d %H:%M:%S')
        transactions['Дата платежа'] = pd.to_datetime(transactions['Дата платежа'], format='%Y-%m-%d %H:%M:%S')

        # Фильтруем транзакции за текущий месяц
        current_month_transactions = filter_current_month_transactions(transactions)

        # Проверяем, что фильтрация работает корректно
        self.assertEqual(len(current_month_transactions), 2)
        self.assertEqual(current_month_transactions.iloc[0]['Дата операции'].date(), datetime(2023, 11, 1).date())
        self.assertEqual(current_month_transactions.iloc[1]['Дата операции'].date(), datetime(2023, 11, 15).date())

if __name__ == '__main__':
    unittest.main()
