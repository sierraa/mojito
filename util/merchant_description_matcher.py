import pandas as pd
from difflib import SequenceMatcher
from fuzzywuzzy import fuzz
from util.merchant_string_cleaner import MerchantStringCleaner

# TODO: consider semantic clustering
class MerchantDescriptionMatcher:

    def __init__(self, confidence_threshold=.70):
        self.string_cleaner = MerchantStringCleaner()
        self.confidence_threshold = confidence_threshold

    def get_labels(self, series):
        clean_data = self.string_cleaner.clean_data(series)
        # TODO: when cleaning data we are still seeing false positives for two descriptions
        # with "market" or "supermarket" -- is there a way to ignore those terms
        # same thing happens with "restaurant"
        clustered_labels = self.__cluster_labels(clean_data)
        return clustered_labels

    @staticmethod
    def get_similarity(w1, w2):
        # TODO: play around with different fuzzywuzzy functions
        return SequenceMatcher(None, w1, w2).ratio()

    def __cluster_labels(self, series):
        # Go through series
        result_set = set()
        for s in series:
            if not result_set:
                result_set.add(s)
            else:
                max_similarity = 0
                for k in result_set:
                    # If confidence is over confidence threshold, add it to list on dict
                    similarity = self.get_similarity(s, k)
                    if similarity > max_similarity:
                        max_similarity = similarity
                if max_similarity < self.confidence_threshold:
                    result_set.add(s)
        return result_set




