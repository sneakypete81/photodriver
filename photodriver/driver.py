from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from .checkbox import Checkbox


class Driver(webdriver.Firefox):
    def __init__(self, headless=False, default_implicit_wait_seconds=2):
        self.download_dir = tempfile.TemporaryDirectory(prefix="photodriver_")

        profile = _profile(self.download_dir.name)
        options = _options(headless)
        super().__init__(profile, options=options)

        self.implicitly_wait(default_implicit_wait_seconds)

    def clear_download_dir(self):
        shutil.rmtree(self.download_dir.name)
        Path(self.download_dir.name).mkdir()

    @property
    def body(self):
        return self.find_element_by_tag_name("body")

    def get_visible_checkboxes(self):
        with self.implicit_wait_context(5):
            elements = self.find_elements_by_xpath(
                "//div[contains(@aria-label, 'Photo - ')]"
            )

        for element in elements:
            try:
                yield Checkbox(self, element)
            except StaleElementReferenceException:
                pass

    @property
    def selection_count(self):
        element = self.find_element_by_xpath("//span[contains(text(), ' selected')]")
        return int(element.text.split(" ")[0])

    def click(self, element):
        element.click()

    def shift_click(self, element, pause_seconds=0.1):
        actions = ActionChains(self)
        actions.move_to_element(element)
        actions.key_down(Keys.SHIFT)
        actions.pause(pause_seconds)
        actions.click(element)
        actions.pause(pause_seconds)
        actions.key_up(Keys.SHIFT)
        actions.perform()

    def implicitly_wait(self, timeout_seconds):
        self._implicit_wait_timeout = timeout_seconds
        super().implicitly_wait(timeout_seconds)

    @contextmanager
    def implicit_wait_context(self, timeout_seconds):
        original_timeout = self._implicit_wait_timeout
        self.implicitly_wait(timeout_seconds)
        yield
        self.implicitly_wait(original_timeout)


def _profile(download_path):
    profile = webdriver.FirefoxProfile()

    preferences = [
        ("browser.download.folderList", 2),
        ("browser.download.dir", download_path),
        ("browser.download.useDownloadDir", True),
        (
            "browser.helperApps.neverAsk.saveToDisk",
            "application/zip;image/jpeg;image/png",
        ),
    ]

    for preference in preferences:
        profile.set_preference(*preference)

    return profile


def _options(headless):
    options = Options()
    options.headless = headless
    return options
