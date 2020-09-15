class MerchantStringCleaner:

    def clean_merchant(self, s):
        clean_str = self.__remove_merchant_junk(s)
        if self.__is_amazon_string(clean_str):
            clean_str = self.__split_amazon_string(clean_str)
        # Remove common special chars, numbers, whitespace, and make lowercase
        clean_str = self.__remove_bad_chars(clean_str)
        return clean_str.lower().strip()

    def clean_data(self, merchants):
        clean_data = set()
        for m in merchants:
            cleaned_string = self.clean_merchant(m)
            clean_data.add(cleaned_string)
        return list(clean_data)

    def __remove_merchant_junk(self, s):
        # Don't care if square was used, pollutes our description
        junk_strings = ["SQUARE      *SQ", "SQU*SQ", "SQ *SQ", "TST*", "SQUARE *SQ *"]
        for junk in junk_strings:
            if junk in s:
                s = s.replace(junk, "")
        return s

    def __split_amazon_string(self, s):
        return s.split("*")[0]

    def __is_amazon_string(self, s):
        amazon_strings = ["Amazon.com", "AMZN MKTP US", "AMZN Mktp US", "AMAZON.COM", "Prime Video", "Kindle Svcs", "AMZN Pickup"]
        for amz in amazon_strings:
            if amz in s:
                return True
        return False

    def __remove_bad_chars(self, s):
        bad_chars = [str(i) for i in range(10)] + ["*", "#", "-"]
        clean_str = ''.join(c for c in s if c not in bad_chars)
        return clean_str