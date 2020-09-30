import pandas as pd

from util.merchant_string_cleaner import MerchantStringCleaner


class TrailheadParser:

    def __init__(self, fname, start_date, end_date):
        self.df = pd.read_csv(fname)
        self.column_name_mapping = {
            # TRNTYPE is special as well as TRANAMT
            "DTPOSTED": "Transaction Date",
        }

    def standardize(self):
        # TODO add a categorize option and use ML from capital one to determine category -- after both have clean strings
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
        self.df["Card No."] = self.df["MEMO"].apply(MerchantStringCleaner.parse_card_no_from_memo)

        # Reformat dates as well

        # Drop unnecessary columns
        self.df = self.df.drop(columns=["TRNTYPE", "TRANAMT", "FITID", "NAME"])
        print(self.df)

    # TODO these should be in a different utility class

if __name__ == "__main__":
    # Delete this lazy ass testing
    parser = TrailheadParser("../trailhead2020.csv", None, None)
    parser.standardize()