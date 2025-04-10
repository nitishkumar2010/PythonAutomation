import time
import re

from pageObjects.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def verify_communities_sorted(price_values, ascending, product_type):
    """Verifies if a list of price values is sorted."""

    if product_type == "community":
        if not price_values:
            raise AssertionError("❌ Price list is empty. Sorting verification failed.")

    numeric_prices = [int(price) for price in price_values]
    sorted_prices = sorted(numeric_prices, reverse=not ascending)

    print(f"Original List: {numeric_prices}")
    print(f"Sorted List: {sorted_prices}")

    assert numeric_prices == sorted_prices, "❌ Failed to verify sorting!"
    print("✅ Verified price list sorted.")

class SearchResultsPage(BasePage):
    """Represents the search results page."""

    def scroll_into_view(self, element):
        """Scrolls the element into view using JavaScript."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def verifyCorrectRedirection(self, chosen_product_name):
        """Verifies correct redirection."""
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, "(.//section[@id='MetroSearch']//div[contains(@aria-label,'Results will filter on the page')]/div/span)[1]")
            )
        )
        redirected_metro_name = self.driver.find_element(
            By.XPATH, "(.//section[@id='MetroSearch']//div[contains(@aria-label,'Results will filter on the page')]/div/span)[1]"
        ).text

        print(f"Redirected: {redirected_metro_name}, Chosen: {chosen_product_name}")
        assert redirected_metro_name == chosen_product_name, "❌ Redirection failed!"
        print("✅ Redirection verified.")

    def _get_price_elements(self, xpath):
        """Helper function to get price elements with explicit wait."""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located((By.XPATH, xpath))
            )
            return self.driver.find_elements(By.XPATH, xpath)
        except TimeoutException:
            print(f"Timeout occurred while finding elements with xpath: {xpath}")
            return []

    def verify_sort_functionality_for_community_cards(self, ascending):
        """Verifies sort functionality for community cards."""
        print("Verifying community card sorting...")
        xpath = ".//*[@id='ProductInfo']//div[text()='Starting From']/../span[not(ancestor::div[contains(@class, 'aos-animate')] and ancestor::div[contains(@class, 'bg-light-blue')])]"
        WebDriverWait(self.driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        product_prices = self._get_price_elements(xpath)

        if product_prices:
            price_values = [re.sub(r"[$,]", "", element.text) for element in product_prices]
            self.scroll_into_view(product_prices[0])
            verify_communities_sorted(price_values, ascending, "community")
        else:
            print("No community card prices found.")

    def verify_master_planned_comm_sort(self, ascending):
        """Verifies master planned community card sorting."""
        print("Verifying MPC sorting...")

        try:
            mpc_xpath = "(.//div[contains(@class,'aos-animate')]//div[contains(@class,'bg-light-blue')])"
            WebDriverWait(self.driver, 120).until(EC.presence_of_all_elements_located((By.XPATH, mpc_xpath)))
            mpc_cards = self.driver.find_elements(By.XPATH, mpc_xpath)

            if mpc_cards:
                self.scroll_into_view(mpc_cards[0])
                for i, card in enumerate(mpc_cards):
                    print(f"Processing MPC card {i + 1} of {len(mpc_cards)}")
                    xpath = f"({mpc_xpath})[{i + 1}]//div[@id='ProductInfo']//div[text()='Starting From']/../span"
                    community_name_xpath = f"({mpc_xpath})[{i + 1}]//div[contains(@class,'text-3xl')]"

                    neighborhood_elements = self._get_price_elements(xpath)
                    community_name_element = self.driver.find_element(By.XPATH, community_name_xpath).text

                    print(f"Found {len(neighborhood_elements)} child communities for {community_name_element} MPC Community.")

                    if neighborhood_elements:
                        price_values = [re.sub(r"[$,]", "", element.text) for element in neighborhood_elements]
                        self.scroll_into_view(neighborhood_elements[0])
                        verify_communities_sorted(price_values, ascending, "mpc")
                    else:
                        print(f"No prices found for MPC card {i + 1}.")
            else:
                print("No MPC cards found.")
        except Exception:
            print("No MPC cards found")

    def apply_sort_option(self, sort_option):
        """Applies a sort option from the dropdown."""
        dropdown_xpath = ".//div[contains(@aria-label,'selector')]//button[contains(@aria-label,'dropdown')]"
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
        self.driver.find_element(By.XPATH, dropdown_xpath).click()

        option_xpath = ".//div[contains(@aria-label,'selector')]/..//button/span"
        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, option_xpath)))
        options = self.driver.find_elements(By.XPATH, option_xpath)

        for option in options:
            if option.text == sort_option:
                option.click()
                return
        print("Sort option not found.")