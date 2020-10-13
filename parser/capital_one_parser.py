import pandas as pd
import math


class CapitalOneParser:

    def __init__(self, fname, start_date=None, end_date=None):
        self.df = pd.read_csv(fname)
        self.transaction_date = 'Transaction Date'
        self.df[self.transaction_date] = pd.to_datetime(self.df[self.transaction_date])
        if start_date and end_date:
            self.df = self.df[(self.df[self.transaction_date] > pd.Timestamp(start_date)) & (
                    self.df[self.transaction_date] < pd.Timestamp(end_date))]
        elif start_date:
            self.df = self.df[(self.df[self.transaction_date] > pd.Timestamp(start_date))]
        elif end_date:
            self.df = self.df[(self.df[self.transaction_date] < pd.Timestamp(end_date))]

    def sum_total_spending(self):
        return self.sum_total_for_dataframe(self.df)

    def sum_total_spending_per_cardholder(self, last_four):
        return self.sum_total_for_dataframe(self.df[self.df["Card No."] == last_four])

    def sum_total_spending_for_dates(self, start_date, end_date):
        date_range = self.df.loc[start_date:end_date]
        return self.sum_total_for_dataframe(date_range)

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
        return self.df['Description'].unique()

    def get_dataframe(self):
        return self.df

    def get_min_date(self):
        return self.df[self.transaction_date].min()

    def get_max_date(self):
        return self.df[self.transaction_date].max()

    def add_data(self, dataframe):
        self.df = self.df.append(dataframe, ignore_index=True)

    def write(self, outfile):
        self.df.to_csv(outfile, index=False)

    def update_categories_for_retailer(self, retailer, new_category):
        self.df.loc[self.df["Description"] == retailer, ["Category"]] = new_category

    def get_unique_transactions_for_category(self, category):
        return self.df.query('Category == "{}"'.format(category))['Description'].unique()

    @staticmethod
    def sum_total_category_for_dataframe(category, dataframe):
        category_df = dataframe.query("Category == '{}'".format(category))
        total = CapitalOneParser.sum_total_for_dataframe(category_df)
        if category == "Income" or category == "Payment/Credit":
            total = abs(total)
        return total

    @staticmethod
    def sum_total_for_dataframe(dataframe):
        remove_nans = lambda x: 0 if math.isnan(x) else x
        total_debits = dataframe["Debit"].apply(remove_nans).sum()
        total_credits = 0 # dataframe["Credit"].apply(remove_nans).sum()
        return total_debits - total_credits
