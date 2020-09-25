import unittest

from util.transaction_date_util import TransactionDateUtil


class TransactionDateUtilTest(unittest.TestCase):

    def test_number_of_months_between_dates(self):
        start_date = "2020-01-01"
        end_date = "2020-12-31"
        num_months = TransactionDateUtil.get_num_months_between_dates(start_date, end_date)
        self.assertEqual(num_months, 11)

    def test_number_of_months_between_dates_zero(self):
        start_date = "2020-01-01"
        end_date = "2020-01-31"
        num_months = TransactionDateUtil.get_num_months_between_dates(start_date, end_date)
        self.assertEqual(num_months, 0)

    def test_number_of_months_between_dates_years(self):
        start_date = "2020-01-01"
        end_date = "2018-01-01"
        num_months = TransactionDateUtil.get_num_months_between_dates(start_date, end_date)
        self.assertEqual(num_months, 24)

    def test_number_of_days_between_dates(self):
        start_date = "2020-01-01"
        end_date = "2020-12-31"
        num_days = TransactionDateUtil.get_num_days_between_dates(start_date, end_date)
        self.assertEqual(num_days, 365)

    def test_number_of_days_between_dates_zero(self):
        start_date = "2020-01-01"
        end_date = "2020-01-01"
        num_days = TransactionDateUtil.get_num_days_between_dates(start_date, end_date)
        self.assertEqual(num_days, 0)

    def test_number_of_weeks_between_dates(self):
        start_date = "2020-01-01"
        end_date = "2020-12-31"
        num_weeks = TransactionDateUtil.get_num_weeks_between_dates(start_date, end_date)
        self.assertEqual(num_weeks, 52)

if __name__ == '__main__':
    unittest.main()
