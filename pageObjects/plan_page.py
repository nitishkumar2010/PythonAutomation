import time
import re

from pageObjects.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PlanPage(BasePage):

    def verifyCorrectRedirection(self, chosenProductName):

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//h1/span"))
        )
        productName = self.driver.find_element(By.XPATH, ".//h1/span")

        redirected_plan_name = productName.text

        print(redirected_plan_name)
        print(chosenProductName)

        assert redirected_plan_name.upper() == chosenProductName.upper(), "❌ Failed to verify that the redirection happens correctly!"
        print("✅ Verified that the redirection happens correctly")


