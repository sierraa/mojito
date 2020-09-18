from parser.capital_one_parser import CapitalOneParser
from parser.merchant_parser import MerchantParser
from util.merchant_description_matcher import MerchantDescriptionMatcher
from util.merchant_string_cleaner import MerchantStringCleaner


class CapitalOneCleaner:

    def __init__(self, fname, start_date=None, end_date=None):
        self.parser = CapitalOneParser(fname, start_date, end_date)
        self.df = self.parser.get_dataframe()
        self.merchant_parser = MerchantParser(self.df)
        self.merchant_cleaner = MerchantStringCleaner()
        self.merchant_matcher = MerchantDescriptionMatcher()
        self.description_column_index = 3

    def clean(self, outfile):
        retailers = self.merchant_parser.get_retailers()
        for i, row in self.df.iterrows():
            desc = self.merchant_cleaner.clean_merchant(row['Description'])
            updated_desc = self.merchant_matcher.find_closest_match(desc, retailers)
            self.df.iat[i, self.description_column_index] = updated_desc
        self.df.to_csv(outfile)