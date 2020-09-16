import re

class MerchantStringCleaner:
    # TODO: take in a csv and output one with cleaned merchants once all the bugs have been worked out here

    def clean_merchant(self, s):
        clean_str = self.remove_merchant_junk(s)
        if self.__is_amazon_string(clean_str):
            clean_str = self.__split_amazon_string(clean_str)
        # Remove common special chars, numbers, whitespace, and make lowercase
        clean_str = self.__remove_bad_chars(clean_str)
        clean_str = clean_str.lower().strip()
        clean_str = self.remove_generic_words(clean_str)
        return clean_str

    def clean_data(self, merchants):
        clean_data = set()
        for m in merchants:
            cleaned_string = self.clean_merchant(m)
            clean_data.add(cleaned_string)
        return list(clean_data)

    @staticmethod
    def remove_merchant_junk(s):
        # Don't care if square was used, pollutes our description
        square_regex = r"((SQUARE)|(SQU)|(SQ))\s*\*{1}(SQ)?\s*\*?\s*"
        junk_strings = ["TST*"]
        s = re.sub(square_regex, '', s)
        for junk in junk_strings:
            if junk in s:
                s = s.replace(junk, "")
        return s

    def remove_generic_words(self, s):
        generic_words = ["restaurant", "tavern", "brewing", "lounge"]
        for generic in generic_words:
            if generic in s:
                s = s.replace(generic, "")
        return s

    def __split_amazon_string(self, s):
        return s.split("*")[0]

    def __is_amazon_string(self, s):
        amazon_strings = ["Amazon.com", "AMZN MKTP US", "AMZN Mktp US", "AMAZON.COM", "Prime Video", "Kindle Svcs", "AMZN Pickup"]
        for amz in amazon_strings:
            if amz in s:
                return True
        return False

    # TODO add some special processing for airbnb as well

    def __remove_bad_chars(self, s):
        bad_chars = [str(i) for i in range(10)] + ["*", "#", "-"]
        clean_str = ''.join(c for c in s if c not in bad_chars)
        return clean_str