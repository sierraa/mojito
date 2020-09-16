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

if __name__ == '__main__':
    unittest.main()
