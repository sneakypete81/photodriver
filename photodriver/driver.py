from pathlib import Path
import shutil
import tempfile

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .checkbox import Checkbox


class Driver(webdriver.Firefox):
    def __init__(self):
        self.download_dir = tempfile.TemporaryDirectory(prefix="photodriver_")

        profile = webdriver.FirefoxProfile()
        for preference in self._get_firefox_preferences():
            profile.set_preference(*preference)

        return super().__init__(profile)

    def clear_download_dir(self):
        shutil.rmtree(self.download_dir.name)
        Path(self.download_dir.name).mkdir()

    def _get_firefox_preferences(self):
        return [
            ("browser.download.folderList", 2),
            ("browser.download.dir", self.download_dir.name),
            ("browser.download.useDownloadDir", True),
            (
                "browser.helperApps.neverAsk.saveToDisk",
                "application/zip;image/jpeg;image/png",
            ),
        ]

    @property
    def body(self):
        return self.find_element_by_tag_name("body")

    @property
    def visible_checkboxes(self):
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
