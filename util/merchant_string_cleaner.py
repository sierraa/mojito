import re

class MerchantStringCleaner:
    # TODO: take in a csv and output one with cleaned merchants once all the bugs have been worked out here
    # TODO: filter out .COM

    def clean_merchant(self, s):
        clean_str = self.remove_merchant_junk(s)
        if self.is_amazon_string(clean_str):
            clean_str = self.split_amazon_string(clean_str)
        elif self.is_airbnb_string(clean_str):
            clean_str = self.split_airbnb_string(clean_str)
        # Remove common special chars, numbers, whitespace, and make lowercase
        clean_str = self.remove_bad_chars(clean_str)
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

    @staticmethod
    def remove_generic_words(s):
        # Still having some issues with market vs supermarket
        generic_words = ["restaurant", "tavern", "brewing", "lounge"]
        for generic in generic_words:
            if generic in s:
                s = s.replace(generic, "")
        return s

    @staticmethod
    def split_amazon_string(s):
        amz_string = s.split("*")[0]
        if amz_string in ["Amazon.com", "AMZN MKTP US", "AMZN Mktp US", "AMAZON.COM", "AMZN Pickup"]:
            return "amazon"
        return amz_string

    @staticmethod
    def is_amazon_string(s):
        amazon_strings = ["Amazon.com", "AMZN MKTP US", "AMZN Mktp US", "AMAZON.COM", "Prime Video", "Kindle Svcs", "AMZN Pickup"]
        for amz in amazon_strings:
            if amz in s:
                return True
        return False

    @staticmethod
    def is_airbnb_string(s):
        return "AIRBNB" in s

    @staticmethod
    def split_airbnb_string(s):
        return s.split(" ")[0]

    @staticmethod
    def remove_bad_chars(s):
        bad_chars = [str(i) for i in range(10)] + ["*", "#", "-"]
        clean_str = ''.join(c for c in s if c not in bad_chars)
        return clean_str