from cli.output_helper import OutputHelper
from main.capital_one_analyzer import CapitalOneAnalyzer


class Analyzer:

    def __init__(self, filename, start_date=None, end_date=None):
        self.output_helper = OutputHelper()
        self.bank = CapitalOneAnalyzer(filename, start_date=start_date, end_date=end_date)

    def analyze(self, verbose):
        spending_per_category = self.bank.get_spending_per_category()
        percentage_per_category = self.bank.get_percentage_per_category()
        total_spending = self.bank.get_total_spending()
        self.output_helper.echo_total(total_spending)
        if verbose:
            self.output_helper.echo_time_averages(self.bank.get_average_monthly_spending(),
                                                  self.bank.get_average_weekly_spending(),
                                                  self.bank.get_average_daily_spending())
        for category in spending_per_category.keys():
            self.output_helper.echo_spending_with_percent(spending_per_category[category], category,
                                                          percentage_per_category[category])
            if verbose:
                self.output_helper.echo_time_averages(self.bank.get_average_monthly_spending_for_category(category),
                                                      self.bank.get_average_weekly_spending_for_category(category),
                                                      self.bank.get_average_daily_spending_for_category(category))

    def analyze_per_cardholder(self, verbose):
        spending_per_category_per_cardholder = self.bank.get_spending_per_category_per_cardholder()
        percent_per_category_per_cardholder = self.bank.get_percent_per_category_per_cardholder()
        for cardholder in spending_per_category_per_cardholder.keys():
            self.output_helper.echo_analyzing_for_cardholder(cardholder)
            if verbose:
                self.output_helper.echo_time_averages(self.bank.get_average_monthly_spending_for_cardholder(cardholder),
                                                      self.bank.get_average_weekly_spending_for_cardholder(cardholder),
                                                      self.bank.get_average_daily_spending_for_cardholder(cardholder))
            for category in spending_per_category_per_cardholder[cardholder].keys():
                self.output_helper.echo_spending_with_percent(
                    spending_per_category_per_cardholder[cardholder][category], category,
                    percent_per_category_per_cardholder[cardholder][category], name=cardholder)
                if verbose:
                    self.output_helper.echo_time_averages(
                        self.bank.get_average_monthly_spending_for_cardholder_for_category(cardholder, category),
                        self.bank.get_average_weekly_spending_for_cardholder_for_category(cardholder, category),
                        self.bank.get_average_weekly_spending_for_cardholder_for_category(cardholder, category))

    def analyze_for_retailer(self, retailer, verbose):
        total_spent = self.bank.get_total_spending()
        self.output_helper.echo_total(total_spent)
        retailer_total = self.bank.get_total_spending_for_retailer(retailer)
        percent = retailer_total / total_spent
        self.output_helper.echo_spending_with_percent(retailer_total, retailer, percent)
        if verbose:
            average, count = self.bank.get_average_and_count_for_retailer(retailer)
            self.output_helper.echo_average_of_transactions(average, count)
            self.output_helper.echo_time_averages(self.bank.get_average_monthly_spending_for_retailer(retailer),
                                                  self.bank.get_average_weekly_spending_for_retailer(retailer),
                                                  self.bank.get_average_daily_spending_for_retailer(retailer))

    def analyze_per_retailer(self, verbose, number_of_retailers, order_by, category=None):
        # TODO: use category option
        # TODO: limit by dollar amount?
        self.output_helper.echo_please_hold()
        total_spent = self.bank.get_total_spending()
        total_per_retailer = self.bank.get_total_spending_per_retailer(order_by)
        retailers = list(total_per_retailer.keys())
        for i in range(min(len(retailers), number_of_retailers)):
            retailer = retailers[i]
            percent = total_per_retailer[retailer] / total_spent
            self.output_helper.echo_spending_with_percent(total_per_retailer[retailer], retailer, percent)
            if verbose:
                self.output_helper.echo_time_averages(self.bank.get_average_monthly_spending_for_retailer(retailer),
                                                      self.bank.get_average_weekly_spending_for_retailer(retailer),
                                                      self.bank.get_average_daily_spending_for_retailer(retailer))
