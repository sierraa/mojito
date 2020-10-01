from collections import namedtuple
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
        self.retailer_metrics = dict()
        self.Retailer = namedtuple('Retailer', 'total count')

    def get_retailers(self):
        if self.retailers:
            return self.retailers
        else:
            return self.matcher.get_labels(self.df['Description'].unique())

    def sum_for_retailer(self, retailer):
        if retailer in self.retailer_metrics.keys():
            return self.retailer_metrics[retailer].total
        similar_retailers = self.__get_similar_retailer_dataframe(retailer)
        # Handle NaNs
        remove_nans = lambda x: 0 if math.isnan(x) else x
        total_debit = similar_retailers["Debit"].apply(remove_nans).sum()
        total_credit = similar_retailers["Credit"].apply(remove_nans).sum()
        # Sum Debits of similar retailers
        total = total_debit - total_credit
        count = similar_retailers.shape[0]
        self.retailer_metrics[retailer] = self.Retailer(total, count)
        return total

    def count_for_retailer(self, retailer):
        if retailer in self.retailer_metrics.keys():
            return self.retailer_metrics[retailer].count
        similar_retailers = self.__get_similar_retailer_dataframe(retailer)
        return similar_retailers.shape[0]

    def __get_similar_retailer_dataframe(self, retailer):
        # Add new column clean description
        self.df['Clean Description'] = self.df['Description'].apply(self.cleaner.clean_merchant)
        # Add a new column similarity
        similarity_func = lambda x: self.matcher.get_similarity(retailer, x)
        self.df['Similarity'] = self.df['Clean Description'].apply(similarity_func)
        # Query for similarity > confidence_level
        similar_retailers = self.df.query('Similarity > {}'.format(self.confidence_level))
        return similar_retailers

