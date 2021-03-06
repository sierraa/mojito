import pandas as pd

from parser.capital_one_parser import CapitalOneParser
from parser.merchant_parser import MerchantParser
from util.memo_string_cleaner import MemoStringCleaner


class TrailheadParser:

    def __init__(self, fname):
        self.df = pd.read_csv(fname)
        self.string_cleaner = MemoStringCleaner()

    def standardize(self, outfile, categorize_file=None):
        # Rewrite trailhead data to a csv that is compatible with the one produced by Capital One
        # TRNTYPE,DTPOSTED,TRANAMT,FITID,NAME,MEMO
        # Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit
        # Make two new columns, Credit and Debit
        self.df["Credit"] = self.df["TRANAMT"]
        debit_query_index = self.df.query("TRNTYPE == 'DEBIT'").index
        self.df.loc[debit_query_index, "Credit"] = ""

        self.df["Debit"] = self.df["TRANAMT"]
        credit_query_index = self.df.query("TRNTYPE == 'CREDIT'").index
        self.df.loc[credit_query_index, "Debit"] = ""
        # Make all values in the column positive
        self.df["Debit"] = self.df["Debit"].apply(lambda x: abs(float(x)) if x else x)

        # Get card number from memo
        self.df["Card No."] = self.df["MEMO"].apply(MemoStringCleaner.parse_card_no_from_memo)

        # Reformat dates as well
        self.df["Transaction Date"] = pd.to_datetime(self.df["DTPOSTED"])
        self.df["Posted Date"] = self.df["Transaction Date"]

        self.df["Description"] = self.df["MEMO"].apply(self.string_cleaner.parse_description)

        if categorize_file:
            self.categorize(categorize_file)
        else:
            self.df["Category"] = pd.Series(["Other" for _ in range(self.df.shape[0])])

        # Drop unnecessary columns
        self.df = self.df.drop(columns=["TRNTYPE", "TRANAMT", "FITID", "NAME", "DTPOSTED", "MEMO"])
        self.df = self.df.reindex(columns=["Transaction Date", "Posted Date", "Card No.", "Description", "Category", "Debit", "Credit"])
        self.df.to_csv(outfile, index=False)

    def categorize(self, categorize_file):
        parser = CapitalOneParser(categorize_file)
        merchant_parser = MerchantParser(parser.df, confidence_level=.87)
        self.df["Category"] = self.df["Description"].apply(merchant_parser.get_category_for_retailer)

