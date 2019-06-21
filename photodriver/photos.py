import pickle
import tempfile
from pathlib import Path

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidCookieDomainException


class Photos:
    URL = "https://photos.google.com"
    TITLE = "Photos - Google Photos"

    def __init__(self):
        self.driver = None
        self._download_dir = tempfile.TemporaryDirectory(prefix="photodriver_download_")

    def set_driver(self, driver):
        self.driver = driver

    def get_firefox_preferences(self):
        return [
            ("browser.download.folderList", 2),
            ("browser.download.dir", self._download_dir.name),
            ("browser.download.useDownloadDir", True),
            ("browser.helperApps.neverAsk.saveToDisk", "application/zip"),
        ]

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

    def select_all(self):
        checkboxes = _get_checkboxes(self.driver)
        if len(checkboxes) == 0:
            return

        checkboxes[0].click()
        if len(checkboxes) == 1:
            return

        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.1)
        wait.until(pressing_key_causes_scroll(Keys.END))

        checkboxes = _get_checkboxes(self.driver)

        actions = ActionChains(self.driver)
        actions.key_down(Keys.SHIFT)
        actions.click(checkboxes[-1])
        actions.key_up(Keys.SHIFT)
        actions.perform()

    def download_selected_photos(self):
        _get_body(self.driver).send_keys(Keys.SHIFT + "D")
        download_file = Path(self._download_dir.name) / "Photos.zip"

        wait = WebDriverWait(self.driver, timeout=60, poll_frequency=0.1)
        wait.until(path_exists(download_file))

        return download_file

    def _get_body(self):
        return self.driver.find_element_by_tag_name("body")


class pressing_key_causes_scroll:
    def __init__(self, key):
        self.key = key

    def __call__(self, driver):
        locations = self._get_checkbox_locations(driver)

        _get_body(driver).send_keys(self.key)

        new_locations = self._get_checkbox_locations(driver)
        return new_locations != locations

    @staticmethod
    def _get_checkbox_locations(driver):
        locations = {}
        for checkbox in _get_checkboxes(driver):
            locations[checkbox] = checkbox.location
        return locations


class path_exists:
    def __init__(self, path):
        self.path = path

    def __call__(self, _):
        return self.path.exists()


def _get_body(driver):
    return driver.find_element_by_tag_name("body")


def _get_checkboxes(driver):
    return driver.find_elements_by_xpath("//div[contains(@aria-label, 'Photo - ')]")
