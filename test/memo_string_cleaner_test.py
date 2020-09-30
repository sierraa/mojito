import unittest

from util.memo_string_cleaner import MemoStringCleaner


class MemoStringCleanerTest(unittest.TestCase):
    def test_parse_out_city_state(self):
        sc = MemoStringCleaner()
        parsed = sc.parse_out_city_state("Hello from PORTLAND OR ")
        self.assertEqual(parsed, "Hello from")

    def test_parse_out_city_state_mixed(self):
        sc = MemoStringCleaner()
        parsed = sc.parse_out_city_state("Welcome to Seattle WA ")
        self.assertEqual(parsed, "Welcome to")

    def test_parse_description(self):
        sc = MemoStringCleaner()
        parsed = sc.parse_description("Withdrawal POS #111122223333 POS MAMA'S DELI TACOMA WA % Card 00 #0000")
        self.assertEqual(parsed, " MAMA'S DELI TACOMA WA ")

    def test_parse_description_with_date(self):
        sc = MemoStringCleaner()
        parsed = sc.parse_description("Withdrawal Credit/Debit Card Signature Debit WARRIOR COFFEE ATLANTA GA Date 01/01/99 2 0000000000 1 1111 % Card 00 #0000")
        self.assertEqual(parsed, " WARRIOR COFFEE ATLANTA GA ")

if __name__ == '__main__':
    unittest.main()
