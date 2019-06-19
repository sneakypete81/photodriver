import pickle
from pathlib import Path

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidCookieDomainException


class Photos:
    URL = "https://photos.google.com"
    TITLE = "Photos - Google Photos"

    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.get(self.URL + "/login")
        if self.driver.title != self.TITLE:
            print("Please sign in to your account using the browser...")
            WebDriverWait(self.driver, 600).until(EC.title_is(self.TITLE))

    def save_cookies(self, filename):
        if not self.driver.current_url.startswith(self.URL):
            self.driver.get(self.URL)

        cookies = self.driver.get_cookies()
        pickle.dump(cookies, open(filename, "wb"))

    def load_cookies(self, filename):
        if not Path(filename).exists():
            return

        if not self.driver.current_url.startswith(self.URL):
            self.driver.get(self.URL)

        for cookie in pickle.load(open(filename, "rb")):
            try:
                self.driver.add_cookie(cookie)
            except InvalidCookieDomainException:
                pass
