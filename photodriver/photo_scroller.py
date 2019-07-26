from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


class PhotoScroller:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=2, poll_frequency=0.1)

    def get_visible_checkboxes(self):
        return list(self.driver.get_visible_checkboxes())

    def to_top(self):
        try:
            self.wait.until(pressing_key_causes_scroll(Keys.HOME))
        except TimeoutException:
            pass

        return self.get_visible_checkboxes()[0]

    def to_bottom(self):
        try:
            self.wait.until(pressing_key_causes_scroll(Keys.END))
        except TimeoutException:
            pass

        return self.get_visible_checkboxes()[-1]

    def focus(self, checkbox):
        while checkbox.element.value_of_css_property("opacity") != "1":
            self.driver.body.send_keys(Keys.TAB)


class pressing_key_causes_scroll:
    def __init__(self, key):
        self.key = key

    def __call__(self, driver):
        original_top = _wait_for_top_checkbox_location(driver)

        driver.body.send_keys(self.key)

        new_top = _wait_for_top_checkbox_location(driver)
        return original_top != new_top


def _get_checkbox_locations(driver):
    locations = []
    for checkbox in driver.get_visible_checkboxes():
        try:
            locations.append((checkbox.label, checkbox.element.location))
        except StaleElementReferenceException:
            pass
    return locations


def _wait_for_top_checkbox_location(driver):
    while True:
        locations = _get_checkbox_locations(driver)
        if locations:
            return locations
