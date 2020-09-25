from datetime import datetime


class TransactionDateUtil:

    @staticmethod
    def validate_dates(start, finish, date_format="%Y-%m-%d"):
        start_date = TransactionDateUtil.validate_date(start, date_format=date_format)
        finish_date = TransactionDateUtil.validate_date(finish, date_format=date_format)
        if start_date > finish_date:
            raise ValueError("Start date cannot be before end date.")

    @staticmethod
    def validate_date(dt, date_format):
        if dt is None:
            return None
        # Raises a value error if date is incorrect
        return datetime.strptime(dt, date_format)

    @staticmethod
    def get_num_months_between_dates(start, finish, date_format="%Y-%m-%d"):
        d1, d2 = datetime.strptime(start, date_format), datetime.strptime(finish, date_format)
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)

    @staticmethod
    def get_num_days_between_dates(start, finish, date_format="%Y-%m-%d"):
        d1, d2 = datetime.strptime(start, date_format), datetime.strptime(finish, date_format)
        delta = d2 - d1
        return abs(delta.days)

    @staticmethod
    def get_num_weeks_between_dates(start, finish, date_format="%Y-%m-%d"):
        return int(TransactionDateUtil.get_num_days_between_dates(start, finish, date_format=date_format) / 7)