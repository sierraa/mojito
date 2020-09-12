#!/usr/bin/env python3

from main.capital_one_analyzer import CapitalOneAnalyzer
# from dotenv import load_dotenv
import sys


def analyze_capital_one(fname):
    capital_one = CapitalOneAnalyzer(fname)
    spending_per_category = capital_one.get_spending_per_category()
    percentage_per_category = capital_one.get_percentage_per_category()
    print("You spent {:.2f} total".format(capital_one.get_total_spending()))
    for category in spending_per_category.keys():
        print(format_spending(spending_per_category[category], category, percentage_per_category[category]))


def format_spending(amount, category, raw_percentage):
    percent = raw_percentage * 100
    return "You spent {:.2f} in {} ({:.2f}% of total)".format(amount, category, percent)


if __name__ == "__main__":
    # load_dotenv()
    # TODO: this is a naive approach
    # Let's turn this into a full CLI!
    account_type = sys.argv[1]
    fname = sys.argv[2]
    if account_type == "capitalone":
        analyze_capital_one(fname)
