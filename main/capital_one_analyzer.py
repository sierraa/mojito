from parser.capital_one_parser import CapitalOneParser


class CapitalOneAnalyzer:

    def __init__(self, fname):
        self.parser = CapitalOneParser(fname)
        self.categories = self.parser.get_categories()
        self.cardholders = self.parser.get_cardholders()
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
