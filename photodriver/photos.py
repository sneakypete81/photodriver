from datetime import timedelta
from pathlib import Path
import pickle
from zipfile import ZipFile

from selenium.common.exceptions import InvalidCookieDomainException
from selenium.webdriver.common.by import By
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

    def login(self, email=None, password=None):
        self.driver.get(self.URL + "/login")

        if email is not None:
            self.driver.find_element_by_id("identifierId").send_keys(email + Keys.ENTER)

            if password is not None:
                WebDriverWait(self.driver, 60).until(
                    EC.visibility_of_element_located((By.NAME, "password"))
                )
                self.driver.find_element_by_name("password").send_keys(
                    password + Keys.ENTER
                )

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

    def download_selected_photos(self, output_path):
        self.driver.body.send_keys(Keys.SHIFT + "D")
        download_file = Path(self.driver.download_dir.name) / "Photos.zip"

        wait = WebDriverWait(self.driver, timeout=60, poll_frequency=0.1)
        wait.until(download_complete(download_file))

        ZipFile(download_file).extractall(output_path)


class download_complete:
    def __init__(self, download_file):
        self.download_file = download_file

    def __call__(self, _):
        part_files = list(self.download_file.parent.glob("*.part"))
        return self.download_file.exists() and part_files == []
