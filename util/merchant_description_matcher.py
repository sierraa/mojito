from difflib import SequenceMatcher
from fuzzywuzzy import process
from util.merchant_string_cleaner import MerchantStringCleaner
import logging


# TODO: consider semantic clustering
class MerchantDescriptionMatcher:

    def __init__(self, confidence_threshold=70):
        self.string_cleaner = MerchantStringCleaner()
        self.confidence_threshold = confidence_threshold

    def get_labels(self, series):
        clean_data = self.string_cleaner.clean_data(series)
        clustered_labels = self.__cluster_labels(clean_data)
        return clustered_labels

    @staticmethod
    def get_similarity(w1, w2):
        # TODO: play around with different fuzzywuzzy functions
        return SequenceMatcher(None, w1, w2).ratio()

    def find_closest_match(self, word, lst):
        match, confidence = process.extractOne(word, lst)
        if confidence < self.confidence_threshold:
            logging.debug(f"No matches found for word {word}")
            raise ValueError(f"No matches found for word {word}")
        return match

    def find_matches(self, word, lst):
        generator = process.extractWithoutOrder(word, lst, score_cutoff=self.confidence_threshold)
        return [item[0] for item in generator]

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




