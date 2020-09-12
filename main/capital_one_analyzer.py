from parser.capital_one import CapitalOneParser


class CapitalOneAnalyzer:

    def __init__(self, fname):
        self.parser = CapitalOneParser(fname)
        self.categories = self.parser.get_categories()
        self.spending_per_category = None
        self.percentage_per_category = None
        self.total_spent = None

    def get_spending_per_category(self):
        if not self.spending_per_category:
            self.spending_per_category = self.__analyze_per_category()
        return self.spending_per_category

    def get_percentage_per_category(self):
        if not self.percentage_per_category:
            self.percentage_per_category = self.__analyze_percentage_of_total_per_category()
        return self.percentage_per_category

    def get_total_spending(self):
        if not self.total_spent:
            self.total_spent = self.parser.sum_total_spending()
        return self.total_spent

    def __analyze_per_category(self):
        # Return a dictionary of spending per category
        spending_per_category = dict()
        for category in self.categories:
            total_for_category = self.parser.sum_total_category(category)
            spending_per_category[category] = total_for_category
        return spending_per_category

    def __analyze_percentage_of_total_per_category(self):
        total = self.parser.sum_total_spending()
        spending_per_category = self.get_spending_per_category()
        percentage_per_category = dict()
        for category in self.categories:
            percentage_per_category[category] = spending_per_category[category] / total
        return percentage_per_category