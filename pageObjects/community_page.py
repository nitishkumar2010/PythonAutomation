import time
import re

from pageObjects.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CommunityPage(BasePage):

    def verifyCorrectRedirection(self, chosenProductName):

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, ".//section[@id='HeaderPlanPage']//h1/span"))
        )
        productName = self.driver.find_element(By.XPATH, ".//section[@id='HeaderPlanPage']//h1/span")

        redirected_community_name = productName.text

        print(redirected_community_name)
        print(chosenProductName)

        assert redirected_community_name == chosenProductName, "❌ Failed to verify that the redirection happens correctly!"
        print("✅ Verified that the redirection happens correctly")


