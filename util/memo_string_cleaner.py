import json
import re


class MemoStringCleaner:
    # Methods for trailhead parsing
    CARD = "% Card"

    def __init__(self):
        # read from json cities.json
        with open('../data/cities.json', 'r') as f:
            self.cities_to_states = json.load(f)
        self.state_abbr_regex = r" (A[KLZR]|C[AOT]|DE|FL|GA|HI|I[DLNA]|K[YS]|M[ETDAISO]|N[JTVEYCM]|O[RHK]|PA|RI|S[CD]|T[XN]|UT|V[AT]|W[AVIY]) "

    @staticmethod
    def parse_card_no_from_memo(s):
        if MemoStringCleaner.CARD not in s:
            return ""
        return s.split("%")[1].split("#")[1]

    def parse_description(self, s):
        atm = "Withdrawal ATM"
        if atm in s:
            return atm
        # More trailhead memo parsing
        s = s.replace("Withdrawal Credit/Debit Card Signature Debit", "")
        pos_regex = r"Withdrawal POS #[0-9]+ POS"
        s = re.sub(pos_regex, '', s)
        address_regex = r"[0-9]{3,6} (SE|SW|NE|NW|N|S|E|W)? [a-zA-Z0-9]+ (RD|AVE?|BLV|ST|CT)?"
        s = re.sub(address_regex, '', s)
        s = re.split(r"Date [0-9]{2}\/[0-9]{2}\/[0-9]{2}", s)[0]
        if self.CARD in s:
            s = s.split(self.CARD)[0]
        s = self.parse_out_city_state(s)
        return s

    def parse_out_city_state(self, s):
        # if a state is in the string, check for cities
        # Only care about USA (sorry)
        match = re.search(self.state_abbr_regex, s)
        if match:
            state = match.group(0).strip()
            cities = self.cities_to_states[state]
            for city in cities:
                city_with_state_upper = city.upper() + " " + state
                city_with_state_mixed = city + " " + state
                if city_with_state_upper in s:
                    s = s.replace(city_with_state_upper, "").strip()
                    break
                elif city_with_state_mixed in s:
                    s = s.replace(city_with_state_mixed, "").strip()
                    break
        return s
