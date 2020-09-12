import pandas as pd
import math

class CapitalOneParser:

    def __init__(self, fname):
        self.df = pd.read_csv(fname)

    def sum_total_spending(self):
        return self.sum_total_spending_for_dataframe(self.df)

    def sum_total_spending_for_dates(self, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_spending_for_dataframe(date_range)

    def sum_total_category(self, category):
        return self.sum_total_category_for_dataframe(category, self.df)

    def sum_total_category_for_dates(self, category, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_category_for_dataframe(category, date_range)

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