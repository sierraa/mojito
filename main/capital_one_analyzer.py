from parser.merchant_parser import MerchantParser
from parser.capital_one_parser import CapitalOneParser
from util.transaction_date_util import TransactionDateUtil


class CapitalOneAnalyzer:

    def __init__(self, fname, category=None, start_date=None, end_date=None):
        self.parser = CapitalOneParser(fname, start_date, end_date)
        self.merchant_parser = MerchantParser(self.parser.get_dataframe(), category=category)
        self.categories = self.parser.get_categories()
        self.cardholders = self.parser.get_cardholders()
        self.min_date = self.parser.get_min_date().to_pydatetime()
        self.max_date = self.parser.get_max_date().to_pydatetime()
        self.num_months = max(TransactionDateUtil.get_num_months_between_dates(self.min_date, self.max_date), 1)
        self.num_weeks = max(TransactionDateUtil.get_num_weeks_between_dates(self.min_date, self.max_date), 1)
        self.num_days = max(TransactionDateUtil.get_num_days_between_dates(self.min_date, self.max_date), 1)
        self.spending_per_category = None
        self.spending_per_category_per_cardholder = None
        self.percent_per_category_per_cardholder = None
        self.percentage_per_category = None
        self.total_spent = None
        self.total_spent_per_cardholder = None

    def get_spending_per_category(self):
        if not self.spending_per_category:
            self.spending_per_category = self.__analyze_per_category()
        return self.spending_per_category

    def get_spending_per_category_per_cardholder(self):
        if not self.spending_per_category_per_cardholder:
            self.spending_per_category_per_cardholder = self.__analyze_per_cardholder()
        return self.spending_per_category_per_cardholder

    def get_percentage_per_category(self):
        if not self.percentage_per_category:
            self.percentage_per_category = self.__analyze_percent_per_category()
        return self.percentage_per_category

    def get_percent_per_category_per_cardholder(self):
        if not self.percent_per_category_per_cardholder:
            self.percent_per_category_per_cardholder = self.__analyze_percent_per_category_per_cardholder()
        return self.percent_per_category_per_cardholder

    def get_total_spending(self):
        if not self.total_spent:
            self.total_spent = self.parser.sum_total_spending()
        return self.total_spent

    def get_total_spending_per_cardholder(self):
        if not self.total_spent_per_cardholder:
            self.total_spent_per_cardholder = dict()
            for cardholder in self.cardholders:
                self.total_spent_per_cardholder[cardholder] = self.parser.sum_total_spending_per_cardholder(cardholder)
        return self.total_spent_per_cardholder

    def get_total_spending_for_retailer(self, retailer):
        # TODO: also keep this in a cache when there is an interactive mode
        return self.merchant_parser.sum_for_retailer(retailer)

    def get_total_spending_per_retailer(self, order_by):
        # Returns sorted dictionary
        # Takes forever TODO: add a progress bar with click
        retailers = self.merchant_parser.get_retailers()
        results = dict()
        for retailer in retailers:
            results[retailer] = self.merchant_parser.sum_for_retailer(retailer)
        if order_by == "number_of_transactions":
            return {k:v for k, v in sorted(results.items(),
                                           key=lambda item: self.merchant_parser.count_for_retailer(item[0]), reverse=True)}
        return {k:v for k, v in sorted(results.items(), key=lambda item: item[1], reverse=True)}

    def get_average_and_count_for_retailer(self, retailer):
        total = self.get_total_spending_for_retailer(retailer)
        count = self.merchant_parser.count_for_retailer(retailer)
        if count > 0:
            return total / count, count
        else:
            return 0, 0

    def get_average_monthly_spending(self):
        return self.get_total_spending() / self.num_months

    def get_average_monthly_spending_for_category(self, category):
        # TODO: need validation around categories
        return self.get_spending_per_category()[category] / self.num_months

    def get_average_monthly_spending_for_retailer(self, retailer):
        return self.get_total_spending_for_retailer(retailer) / self.num_months

    def get_average_monthly_spending_for_cardholder(self, cardholder):
        return self.get_total_spending_per_cardholder()[cardholder] / self.num_months

    def get_average_weekly_spending(self):
        return self.get_total_spending() / self.num_weeks

    def get_average_weekly_spending_for_category(self, category):
        return self.get_spending_per_category()[category] / self.num_weeks

    def get_average_weekly_spending_for_retailer(self, retailer):
        return self.get_total_spending_for_retailer(retailer) / self.num_weeks

    def get_average_weekly_spending_for_cardholder(self, cardholder):
        return self.get_total_spending_per_cardholder()[cardholder] / self.num_weeks

    def get_average_daily_spending(self):
        return self.get_total_spending() / self.num_days

    def get_average_daily_spending_for_category(self, category):
        return self.get_spending_per_category()[category] / self.num_days

    def get_average_daily_spending_for_retailer(self, retailer):
        return self.get_total_spending_for_retailer(retailer) / self.num_days

    def get_average_daily_spending_for_cardholder(self, cardholder):
        return self.get_total_spending_per_cardholder()[cardholder] / self.num_days

    def __analyze_per_category(self):
        # Return a dictionary of spending per category
        spending_per_category = dict()
        for category in self.categories:
            total_for_category = self.parser.sum_total_category(category)
            spending_per_category[category] = total_for_category
        return spending_per_category

    def __analyze_per_cardholder(self):
        spending_per_cardholder = dict()
        for cardholder in self.cardholders:
            spending_per_cardholder[cardholder] = dict()
            for category in self.categories:
                total_for_category = self.parser.sum_total_category_per_cardholder(category, cardholder)
                spending_per_cardholder[cardholder][category] = total_for_category
        return spending_per_cardholder

    def __analyze_percent_per_category(self):
        total = self.get_total_spending()
        spending_per_category = self.get_spending_per_category()
        percentage_per_category = dict()
        for category in self.categories:
            percentage_per_category[category] = spending_per_category[category] / total
        return percentage_per_category

    def __analyze_percent_per_category_per_cardholder(self):
        percent_per_category_per_cardholder = dict()
        spending_per_category_per_cc = self.get_spending_per_category_per_cardholder()
        for cardholder in self.cardholders:
            total = self.get_total_spending_per_cardholder()[cardholder]
            percent_per_category_per_cardholder[cardholder] = dict()
            for category in self.categories:
                percent_per_category_per_cardholder[cardholder][category] = spending_per_category_per_cc[cardholder][category] / total
        return percent_per_category_per_cardholder
