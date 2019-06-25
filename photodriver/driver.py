import tempfile
from selenium import webdriver

from .checkbox import Checkbox


class Driver(webdriver.Firefox):
    def __init__(self):
        self.download_dir = tempfile.TemporaryDirectory(prefix="photodriver_")

        profile = webdriver.FirefoxProfile()
        for preference in self._get_firefox_preferences():
            profile.set_preference(*preference)

        return super().__init__(profile)

    def _get_firefox_preferences(self):
        return [
            ("browser.download.folderList", 2),
            ("browser.download.dir", self.download_dir.name),
            ("browser.download.useDownloadDir", True),
            ("browser.helperApps.neverAsk.saveToDisk", "application/zip"),
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
            yield Checkbox(element)

    @property
    def selection_count(self):
        element = self.find_element_by_xpath("//span[contains(text(), ' selected')]")
        return int(element.text.split(" ")[0])
