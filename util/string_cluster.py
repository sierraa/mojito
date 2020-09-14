import pandas as pd
from difflib import SequenceMatcher


class MerchantDescriptionMatcher:

    def cluster_strings(self, series):
        clean_data = self.__clean_data(series)
        # TODO: when cleaning data we are still seeing false positives for two descriptions
        # with "market" or "supermarket" -- is there a way to ignore those terms
        distances = self.__compute_distances(clean_data)

    def __clean_data(self, series):
        # TODO: make this its own class
        junk_strings = ["SQUARE      *SQ", "SQU*SQ", "SQ *SQ"]
        bad_chars = [str(i) for i in range(10)] + ["*", "#", "-"]
        clean_data = set() # Duplicates likely to occur during cleanup
        for s in series:
            clean_str = s
            # Don't care if square was used, pollutes our description
            for junk in junk_strings:
                if junk in clean_str:
                    clean_str = clean_str.replace(junk, "")
            # Remove common special chars, numbers, whitespace, and make lowercase
            clean_str = ''.join(c for c in clean_str if c not in bad_chars)
            clean_str = clean_str.lower().strip()
            clean_data.add(clean_str)
        return list(clean_data)

    def __compute_distances(self, series):
        df = pd.DataFrame(0.0, index=series, columns=series)
        for s1 in series:
            for s2 in series:
                distance = self.__get_distance(s1, s2)
                df.at[s1, s2] = distance
        return df

    def __cluster(self, series, similarities):
        # TODO determine which algorithm is best
        pass

    def __get_distance(self, w1, w2):
        return SequenceMatcher(None, w1, w2).ratio()


# if __name__ == "__main__":
#     # TODO: delete this, just for testing
#     data = pd.read_csv('../2019.csv')
#     merchandise_merchants = data[data['Category']=='Merchandise']['Description'].unique()
#     sc = MerchantDescriptionMatcher()
#     sc.cluster_strings(merchandise_merchants)