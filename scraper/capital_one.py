from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class CapitalOne:

    def login(self, username, password):
        browser = webdriver.Firefox()
        browser.get("https://capitalone.com")

        username_input = browser.find_element_by_id("noAcctUid")
        username_input.send_keys(username)
        time.sleep(2)

        password_input = browser.find_element_by_id("noAcctPw")
        password_input.send_keys(password_input)
        password_input.send_keys(Keys.RETURN)


