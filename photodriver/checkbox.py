from dateutil.parser import parse
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class Checkbox:
    def __init__(self, element):
        self.element = element
        self.label = element.get_attribute("aria-label")
        date_string = self.label.split("-")[-1]
        self.date = parse(date_string).date()

    def click(self):
        self.element.click()

    def shift_click(self):
        actions = ActionChains(self.element.parent)
        actions.key_down(Keys.SHIFT)
        actions.pause(0.5)
        actions.click(self.element)
        actions.pause(0.5)
        actions.key_up(Keys.SHIFT)
        actions.perform()
