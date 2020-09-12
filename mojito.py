#!/usr/bin/env python3

from parser.capital_one import CapitalOneParser
# from dotenv import load_dotenv
import sys

if __name__ == "__main__":
    # load_dotenv()
    # TODO: this is a naive approach
    filename = sys.argv[1]
    capital_one = CapitalOneParser(filename)
    total_spending = capital_one.sum_total_spending()
    print("You spent {} total".format(total_spending))
    total_lodging = capital_one.sum_total_category("Lodging")
    print("You spent {} on lodging.".format(total_lodging))
    total_dining = capital_one.sum_total_category("Dining")
    print("You spent {} on dining.".format(total_dining))
