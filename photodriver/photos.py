from datetime import date, timedelta, MINYEAR
from pathlib import Path
import pickle
import shutil
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
            password_field = self.driver.find_element_by_name("password")
            password_field.send_keys(password)
            self.driver.find_element_by_id("passwordNext").click()

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
        if start_date is None:
            first_date = date(day=1, month=1, year=MINYEAR)
        else:
            first_date = start_date

        if stop_date is None:
            last_date = date.today()
        else:
            last_date = stop_date - timedelta(days=1)

        self._search(first_date, last_date)

        checkboxes = self.scroll.get_visible_checkboxes()
        if len(checkboxes) == 0:
            return 0

        self.driver.shift_click(self.driver.body)
        top_checkbox = checkboxes[0]
        self.scroll.focus(top_checkbox)
        self.driver.body.send_keys(" ")
        top_checkbox.click()

        if len(checkboxes) == 1:
            return 1

        bottom_checkbox = self.scroll.to_bottom()
        bottom_checkbox.shift_click()

        return self.driver.selection_count

    def download_selected_photos(self, output_path):
        self.driver.clear_download_dir()
        download_path = Path(self.driver.download_dir.name)

        self.driver.body.send_keys(Keys.SHIFT + "D")

        wait = WebDriverWait(self.driver, timeout=60, poll_frequency=0.1)
        wait.until(download_complete(download_path))

        files = list(download_path.iterdir())

        if files == [download_path / "Photos.zip"]:
            self._extract_and_delete_zip(files[0])
            files = list(download_path.iterdir())

        for f in files:
            shutil.copy(f, output_path)

    def _search(self, first_date, last_date):
        first_string = first_date.strftime("%-d %B %Y")
        last_string = last_date.strftime("%-d %B %Y")
        self.driver.get(self.URL + f"/search/{first_string} - {last_string}")

    @staticmethod
    def _extract_and_delete_zip(zip):
        ZipFile(zip).extractall(zip.parent)
        zip.unlink()


class download_complete:
    def __init__(self, download_dir):
        self.download_dir = Path(download_dir)

    def __call__(self, _):
        files = list(self.download_dir.iterdir())
        if files == []:
            return False
        if any([f.suffix == ".part" for f in files]):
            return False
        return True
