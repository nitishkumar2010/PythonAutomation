from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_element(self, locator):
        """Waits and clicks on an element."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        """Finds an input field and enters text."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def enter_text_one_by_one(self, locator, text):
        """Finds an input field and enters text."""
        time.sleep(2)
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(1.5)

    def get_elements(self, locator):
        """Finds multiple elements."""
        return self.driver.find_elements(*locator)
