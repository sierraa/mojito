import pandas as pd
import math


class CapitalOneParser:

    def __init__(self, fname):
        self.df = pd.read_csv(fname)

    def sum_total_spending(self):
        return self.sum_total_spending_for_dataframe(self.df)

    def sum_total_spending_per_cardholder(self, last_four):
        return self.sum_total_spending_for_dataframe(self.df[self.df["Card No."] == last_four])

    def sum_total_spending_for_dates(self, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_spending_for_dataframe(date_range)

    def sum_total_category(self, category):
        return self.sum_total_category_for_dataframe(category, self.df)

    def sum_total_category_for_dates(self, category, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_category_for_dataframe(category, date_range)

    def sum_total_category_per_cardholder(self, category, last_four):
        return self.sum_total_category_for_dataframe(category, self.df[self.df["Card No."] == last_four])

    def get_categories(self):
        return self.df['Category'].unique()

    def get_cardholders(self):
        return self.df['Card No.'].unique()

    def get_merchants(self):
        # TODO: clean this data before returning
        return self.df['Description'].unique()

    @staticmethod
    def sum_total_category_for_dataframe(category, dataframe):
        # TODO: this is a naive approach, would like to get more granular
        # And use pandas more effectively
        total = 0
        for _, row in dataframe.iterrows():
            if row['Category'] == category:
                debit = float(row['Debit'])
                if not math.isnan(debit): # A credit will have the debit column set as NaN
                    total += debit
        return total

    @staticmethod
    def sum_total_spending_for_dataframe(dataframe):
        total = 0
        for _, row in dataframe.iterrows():
            debit = float(row['Debit'])
            if not math.isnan(debit):
                total += debit
        return total