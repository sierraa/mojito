from datetime import datetime


class TransactionDateUtil:

    @staticmethod
    def validate_dates(start: str, finish: str, date_format="%Y-%m-%d"):
        start_date = TransactionDateUtil.validate_date(start, date_format=date_format)
        finish_date = TransactionDateUtil.validate_date(finish, date_format=date_format)
        if start_date > finish_date:
            raise ValueError("Start date cannot be before end date.")

    @staticmethod
    def validate_date(dt: str, date_format: str):
        if dt is None:
            return None
        # Raises a value error if date is incorrect
        return datetime.strptime(dt, date_format)

    @staticmethod
    def get_num_months_between_dates(d1: datetime, d2: datetime):
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)

    @staticmethod
    def get_num_days_between_dates(d1: datetime, d2: datetime):
        delta = d2 - d1
        return abs(delta.days)

    @staticmethod
    def get_num_weeks_between_dates(d1: datetime, d2: datetime):
        return int(TransactionDateUtil.get_num_days_between_dates(d1, d2) / 7)