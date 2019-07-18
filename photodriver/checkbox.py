from dateutil.parser import parse


class Checkbox:
    def __init__(self, driver, element):
        self.driver = driver
        self.element = element
        self.label = element.get_attribute("aria-label")
        date_string = self.label.split("-")[-1]
        self.date = parse(date_string).date()

    def click(self):
        self.element.click()

    def shift_click(self):
        self.driver.shift_click(self.element)
