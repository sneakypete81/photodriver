from datetime import timedelta
from pathlib import Path
import pickle

from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .photo_scroller import PhotoScroller


class Photos:
    URL = "https://photos.google.com"
    TITLE = "Photos - Google Photos"

    def __init__(self, driver):
        self.driver = driver
        self.scroll = PhotoScroller(driver)

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

    def select_range(self, start_date, stop_date):
        self.driver.body.click()
        checkboxes = self.scroll.get_visible_checkboxes()

        if len(checkboxes) == 0:
            return 0

        last_checkbox = self.scroll.to_bottom()

        if start_date is None:
            start_checkbox = last_checkbox
        else:
            start_checkbox = self.scroll.up_to_checkbox(start_date)

        start_checkbox.click()

        if len(checkboxes) == 1:
            return 1

        if stop_date is None:
            stop_checkbox = self.scroll.to_top()
        else:
            one_day = timedelta(days=1)
            self.scroll.up_to_checkbox(stop_date)
            stop_checkbox = self.scroll.down_to_checkbox(stop_date - one_day)

        stop_checkbox.shift_click()

        return self.driver.selection_count

    def download_selected_photos(self):
        self.driver.body.send_keys(Keys.SHIFT + "D")
        download_file = Path(self.driver.download_dir.name) / "Photos.zip"

        wait = WebDriverWait(self.driver, timeout=60, poll_frequency=0.1)
        wait.until(path_exists(download_file))

        return download_file


class path_exists:
    def __init__(self, path):
        self.path = path

    def __call__(self, _):
        return self.path.exists()
