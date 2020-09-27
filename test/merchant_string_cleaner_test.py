import unittest

from util.merchant_string_cleaner import MerchantStringCleaner


class MerchantStringCleanerTest(unittest.TestCase):
    def test_square_strings(self):
        string_cleaner = MerchantStringCleaner()
        rain_or_shine = string_cleaner.remove_merchant_junk("SQU*SQ *RAIN OR SHINE")
        self.assertEqual(rain_or_shine, "RAIN OR SHINE")
        por_que_no = string_cleaner.remove_merchant_junk("SQ *SQ * POR QUE NO")
        self.assertEqual(por_que_no, "POR QUE NO")
        nova_coffee = string_cleaner.remove_merchant_junk("SQ     *SQ *NOVA COFFEE")
        self.assertEqual(nova_coffee, "NOVA COFFEE")
        glitch = string_cleaner.remove_merchant_junk("SQ*GLITCH")
        self.assertEqual(glitch, "GLITCH")
        baris = string_cleaner.remove_merchant_junk("SQUARE      *SQ *BARIS")
        self.assertEqual(baris, "BARIS")
        ecdysiast = string_cleaner.remove_merchant_junk("SQUARE *SQ *ECDYSIAST")
        self.assertEqual(ecdysiast, "ECDYSIAST")

    def test_tst_strings(self):
        string_cleaner = MerchantStringCleaner()
        garden_bar = string_cleaner.remove_merchant_junk("TST* GARDEN BAR")
        self.assertEqual(garden_bar, " GARDEN BAR")

    def test_com_strings(self):
        string_cleaner = MerchantStringCleaner()
        target = string_cleaner.remove_merchant_junk("TARGET.COM")
        self.assertEqual(target, "TARGET")

    def test_is_amazon_string(self):
        string_cleaner = MerchantStringCleaner()
        amazon_strings = ["AMZN Mktp US*KX5GE4S83", "AMAZON.COM*2I0LK9TD3", "Amazon.com*539HF0JE3",
                          "Prime Video*JT7KI4PV3", "Kindle Svcs*5J0Y09EZ3"]
        non_amazon_strings = ["THE HOME DEPOT #0000", "WALGREENS #1111", "MULTNOMAH COUNTY CARVE"]
        for s in amazon_strings:
            self.assertTrue(string_cleaner.is_amazon_string(s))
        for s in non_amazon_strings:
            self.assertFalse(string_cleaner.is_amazon_string(s))

    def test_split_airbnb_string(self):
        string_cleaner = MerchantStringCleaner()
        airbnb_strings = ["AIRBNB * ABCDEFGH", "AIRBNB  XYZABCLMNOP", "AIRBNB"]
        for s in airbnb_strings:
            self.assertEqual(string_cleaner.split_airbnb_string(s), "AIRBNB")

if __name__ == '__main__':
    unittest.main()
