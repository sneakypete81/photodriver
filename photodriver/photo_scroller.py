from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class PhotoScroller:
    def __init__(self, driver):
        self.driver = driver

    def get_visible_checkboxes(self):
        return list(self.driver.visible_checkboxes)

    def to_top(self):
        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.1)
        wait.until(pressing_key_causes_scroll(Keys.HOME))

        return self.get_visible_checkboxes()[0]

    def to_bottom(self):
        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.1)
        wait.until(pressing_key_causes_scroll(Keys.END))

        return self.get_visible_checkboxes()[-1]

    def up_to_checkbox(self, date):
        while True:
            for checkbox in reversed(self.get_visible_checkboxes()):
                if checkbox.date >= date:
                    return checkbox

            wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.1)
            wait.until(pressing_key_causes_scroll(Keys.PAGE_UP))


class pressing_key_causes_scroll:
    def __init__(self, key):
        self.key = key

    def __call__(self, driver):
        locations = self._get_checkbox_locations(driver)

        driver.body.send_keys(self.key)

        new_locations = self._get_checkbox_locations(driver)
        return new_locations != locations

    @staticmethod
    def _get_checkbox_locations(driver):
        locations = {}
        for checkbox in driver.visible_checkboxes:
            locations[checkbox.label] = checkbox.element.location
        return locations
