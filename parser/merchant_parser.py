import math
from util.merchant_description_matcher import MerchantDescriptionMatcher
from util.merchant_string_cleaner import MerchantStringCleaner


class MerchantParser:
    # For getting detailed data for a merchant

    def __init__(self, df, confidence_level=0.70, category=None):
        self.df = df[df['Category'] == category] if category else df
        self.matcher = MerchantDescriptionMatcher()
        self.cleaner = MerchantStringCleaner()
        self.confidence_level = confidence_level
        self.category = category
        self.retailers = None

    def get_retailers(self):
        if self.retailers:
            return self.retailers
        else:
            return self.matcher.get_labels(self.df['Description'].unique())

    def sum_for_retailer(self, retailer):
        total = 0.0
        for _, row in self.df.iterrows():
            description = row['Description']
            clean_desc = self.cleaner.clean_merchant(description)
            if self.matcher.get_similarity(retailer, clean_desc) > self.confidence_level:
                debit = float(row['Debit'])
                if not math.isnan(debit): # A credit will have the debit column set as NaN
                    total += debit
        return total

    def count_for_retailer(self, retailer):
        count = 0
        for _, row in self.df.iterrows():
            description = row['Description']
            clean_desc = self.cleaner.clean_merchant(description)
            if self.matcher.get_similarity(retailer, clean_desc) > self.confidence_level:
                debit = float(row['Debit'])
                if not math.isnan(debit): # A credit will have the debit column set as NaN
                    count += 1
        return count
