import time
import re

from pageObjects.base_page import BasePage
from utils.locators import SearchResultsPageLocators
from utils.helpers import click_first_or_second_element, is_clickable
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class QMIPage(BasePage):

    def verifyCorrectRedirection(self, chosenProductName):

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//h1/span"))
        )
        productName = self.driver.find_element(By.XPATH, ".//h1/span")

        redirected_qmi_name = productName.text

        print(redirected_qmi_name)
        print(chosenProductName)

        assert redirected_qmi_name.upper() == chosenProductName.upper(), "❌ Failed to verify that the redirection happens correctly!"
        print("✅ Verified that the redirection happens correctly")


