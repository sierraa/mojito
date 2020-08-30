#!/usr/bin/env python3

from scraper.capital_one import CapitalOne
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    capital_one_user = os.getenv("CAPITAL_ONE_USERNAME")
    capital_one_password = os.getenv("CAPITAL_ONE_PASSWORD")
    capital_one = CapitalOne()
    capital_one.login(capital_one_user, capital_one_password)
