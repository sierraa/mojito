from main.capital_one_cleaner import CapitalOneCleaner
from parser.capital_one_parser import CapitalOneParser


class Cleaner:
    """
    This is a hodgepodge utility class right now, watch this space and break out new classes as needed
    """
    @staticmethod
    def merge_data(initial_fname, csvs, output):
        initial_data = CapitalOneParser(initial_fname)
        for fname in csvs:
            new_data = CapitalOneParser(fname)
            initial_data.add_data(new_data.get_dataframe())
        initial_data.write(output)

    @staticmethod
    def clean_capital_one(input, output):
        capital_one_cleaner = CapitalOneCleaner(input)
        capital_one_cleaner.clean(output)