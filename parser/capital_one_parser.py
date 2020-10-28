import pandas as pd
import numpy as np
import math
from util.constants import INCOME, CATEGORY, PAYMENT_CREDIT, TRANSACTION_DATE, CARD_NO, DESCRIPTION, DEBIT, CREDIT


class CapitalOneParser:

    def __init__(self, fname, start_date=None, end_date=None):
        self.df = pd.read_csv(fname)
        # Store incomes and payments records separately
        self.__set_up_incomes_and_payments()

        self.df[TRANSACTION_DATE] = pd.to_datetime(self.df[TRANSACTION_DATE])
        if start_date and end_date:
            self.df = self.df[(self.df[TRANSACTION_DATE] > pd.Timestamp(start_date)) & (
                    self.df[TRANSACTION_DATE] < pd.Timestamp(end_date))]
        elif start_date:
            self.df = self.df[(self.df[TRANSACTION_DATE] > pd.Timestamp(start_date))]
        elif end_date:
            self.df = self.df[(self.df[TRANSACTION_DATE] < pd.Timestamp(end_date))]

    def sum_total_income(self):
        income = self.sum_total_category_for_dataframe(INCOME, self.incomes_and_payments_df)
        return abs(income)

    def sum_total_income_for_source(self, source):
        income_source_df = self.incomes_and_payments_df.query("Category == @INCOME").query("Description == @source")
        return self.sum_total_for_dataframe(income_source_df)

    def sum_total_payment_credit(self):
        return self.sum_total_category_for_dataframe(PAYMENT_CREDIT, self.incomes_and_payments_df)

    def sum_total_spending(self):
        return self.sum_total_for_dataframe(self.df)

    def sum_total_spending_per_cardholder(self, last_four):
        return self.sum_total_for_dataframe(self.df[self.df[CARD_NO] == last_four])

    def sum_total_spending_for_dates(self, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_for_dataframe(date_range)

    def sum_total_category(self, category):
        return self.sum_total_category_for_dataframe(category, self.df)

    def sum_total_category_for_dates(self, category, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_category_for_dataframe(category, date_range)

    def sum_total_category_per_cardholder(self, category, last_four):
        return self.sum_total_category_for_dataframe(category, self.df[self.df[CARD_NO] == last_four])

    def get_categories(self):
        return self.df[CATEGORY].unique()

    def get_all_categories(self):
        spending_categories = self.df[CATEGORY].unique()
        income_categories = self.incomes_and_payments_df[CATEGORY].unique()
        return np.concatenate((spending_categories, income_categories), axis=None)

    def get_cardholders(self):
        return self.df[CARD_NO].unique()

    def get_merchants(self):
        return self.df[DESCRIPTION].unique()

    def get_dataframe(self):
        return self.df

    def get_min_date(self):
        return self.df[TRANSACTION_DATE].min()

    def get_max_date(self):
        return self.df[TRANSACTION_DATE].max()

    def get_income_sources(self):
        income = self.incomes_and_payments_df.query("Category == @INCOME")
        return income[DESCRIPTION].unique()

    def add_data(self, dataframe):
        self.df = self.df.append(dataframe, ignore_index=True)

    def write(self, outfile):
        combined_transactions = self.df.append(self.incomes_and_payments_df, ignore_index=True)
        combined_transactions.to_csv(outfile, index=False)

    def update_categories_for_retailer(self, retailer, new_category):
        self.df.loc[self.df[DESCRIPTION] == retailer, [CATEGORY]] = new_category

    def get_unique_transactions_for_category(self, category):
        if category == INCOME or category == PAYMENT_CREDIT:
            return self.incomes_and_payments_df.query('Category == @category')[DESCRIPTION].unique()
        return self.df.query('Category == @category')[DESCRIPTION].unique()

    @staticmethod
    def sum_total_category_for_dataframe(category, dataframe):
        category_df = dataframe.query(f"Category == '{category}'")
        total = CapitalOneParser.sum_total_for_dataframe(category_df)
        return total

    @staticmethod
    def sum_total_for_dataframe(dataframe):
        remove_nans = lambda x: 0 if math.isnan(x) else x
        total_debits = dataframe[DEBIT].apply(remove_nans).sum()
        total_credits = dataframe[CREDIT].apply(remove_nans).sum()
        return total_debits - total_credits

    def __set_up_incomes_and_payments(self):
        self.incomes_and_payments_df = self.df.query("Category == @INCOME")
        payments = self.df.query("Category == @PAYMENT_CREDIT")
        self.incomes_and_payments_df = self.incomes_and_payments_df.append(payments)
        self.df = self.df.query("Category != @INCOME").query("Category != @PAYMENT_CREDIT")