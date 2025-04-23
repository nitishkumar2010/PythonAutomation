import time
import re

from pageObjects.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from utils.locators import SearchResultsLocators

def verify_product_cards_sorted(price_values, ascending, product_type):
    """Verifies if a list of price values is sorted."""

    if product_type == "community" or product_type == "plans":
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
            EC.presence_of_element_located(SearchResultsLocators.REDIRECTION_METRO_NAME)
        )
        redirected_metro_name = self.driver.find_element(*SearchResultsLocators.REDIRECTION_METRO_NAME).text

        print(f"Redirected: {redirected_metro_name}, Chosen: {chosen_product_name}")
        assert redirected_metro_name == chosen_product_name, "❌ Redirection failed!"
        print("✅ Redirection verified.")

    def _get_price_elements(self, locator):
        """Helper function to get price elements with explicit wait."""
        try:
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located(locator)
            )
            return self.driver.find_elements(*locator)
        except TimeoutException:
            print(f"Timeout occurred while finding elements with locator: {locator}")
            return []

    def verify_sort_functionality_for_community_cards(self, ascending):
        """Verifies sort functionality for community cards."""
        print("Verifying community card sorting...")
        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(SearchResultsLocators.COMMUNITY_CARD_PRICES))
        product_prices = self._get_price_elements(SearchResultsLocators.COMMUNITY_CARD_PRICES)

        if product_prices:
            price_values = [re.sub(r"[$,]", "", element.text) for element in product_prices]
            self.scroll_into_view(product_prices[0])
            verify_product_cards_sorted(price_values, ascending, "community")
        else:
            print("No community card prices found.")

    def verify_sort_functionality_for_plan_cards(self, ascending):

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(SearchResultsLocators.PLAN_TAB))
        plan_tab = self.driver.find_element(*SearchResultsLocators.PLAN_TAB)
        plan_tab.click()

        """Verifies sort functionality for community cards."""
        print("Verifying plan card sorting...")
        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(SearchResultsLocators.PLAN_CARD_PRICES))
        product_prices = self._get_price_elements(SearchResultsLocators.PLAN_CARD_PRICES)

        if product_prices:
            price_values = [re.sub(r"[$,]", "", element.text) for element in product_prices]
            self.scroll_into_view(product_prices[0])
            verify_product_cards_sorted(price_values, ascending, "plans")
        else:
            print("No community card prices found.")

    def verify_master_planned_comm_sort(self, ascending):
        """Verifies master planned community card sorting."""
        print("Verifying MPC sorting...")

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(SearchResultsLocators.MPC_CARDS))
            mpc_cards = self.driver.find_elements(*SearchResultsLocators.MPC_CARDS)

            if mpc_cards:
                self.scroll_into_view(mpc_cards[0])
                for i, card in enumerate(mpc_cards):
                    print(f"Processing MPC card {i + 1} of {len(mpc_cards)}")
                    neighborhood_elements = self._get_price_elements(SearchResultsLocators.MPC_CARD_PRICE(i))
                    community_name_element = self.driver.find_element(*SearchResultsLocators.MPC_CARD_COMMUNITY_NAME(i)).text

                    print(f"Found {len(neighborhood_elements)} child communities for {community_name_element} MPC Community.")

                    if neighborhood_elements:
                        price_values = [re.sub(r"[$,]", "", element.text) for element in neighborhood_elements]
                        self.scroll_into_view(neighborhood_elements[0])
                        verify_product_cards_sorted(price_values, ascending, "mpc")
                    else:
                        print(f"No prices found for MPC card {i + 1}.")
            else:
                print("No MPC cards found.")
        except Exception:
            print("No MPC cards found")

    def apply_sort_option(self, sort_option):
        """Applies a sort option from the dropdown."""
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located(SearchResultsLocators.SORT_DROPDOWN))
        self.driver.find_element(*SearchResultsLocators.SORT_DROPDOWN).click()

        WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(SearchResultsLocators.SORT_OPTIONS))
        options = self.driver.find_elements(*SearchResultsLocators.SORT_OPTIONS)

        for option in options:
            if option.text == sort_option:
                option.click()
                return
        print("Sort option not found.")