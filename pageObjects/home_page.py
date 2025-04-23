import random

from selenium.webdriver import ActionChains

from utils.locators import HomePageLocators
from utils.logger import logger
from pageObjects.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HomePage(BasePage):

    def scroll_into_view(self, element):
        """Scroll the element into view using JavaScript."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def search(self, text, search_type):
        """Performs a search operation."""

        self.enter_text_one_by_one(HomePageLocators.SEARCH_BOX, text)
        print("Executing search function...")  # Debugging

        # Adjusting wait to make sure elements are visible
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located(HomePageLocators.ANIMATED_DIVS)
        )

        suggestions = self.get_locator_value(search_type)
        return self.click_on_suggestion(text, suggestions, search_type)

    def click_on_location_from_FYH_header(self, location):
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located(HomePageLocators.FIND_YOUR_DREAM_HOME_BUTTON)
        )

        fydh_button = self.driver.find_element(*HomePageLocators.FIND_YOUR_DREAM_HOME_BUTTON)
        fydh_button.click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_all_elements_located(HomePageLocators.PREFETCH_BUTTONS)
        )

        all_locations = self.driver.find_elements(*HomePageLocators.PREFETCH_BUTTONS)
        location_found = False  # Add a flag to track if the location is found

        for element in all_locations:
            if location == element.text:
                element.click()
                location_found = True  # Set the flag to True.
                break  # Exit loop once location is found

        if not location_found:  # Check the flag after the loop.
            print("Related location was not found")

    def get_locator_value(self, suggestion_type):
        """Returns a list of elements based on the suggestion type."""
        locators = {
            "community": HomePageLocators.COMMUNITY_SUGGESTIONS,
            "qmi": HomePageLocators.QMI_SUGGESTIONS,
            "plan": HomePageLocators.PLAN_SUGGESTIONS,
            "market": HomePageLocators.MARKET_SUGGESTIONS
        }

        locator = locators.get(suggestion_type, None)
        if not locator:
            print(f"Invalid suggestion type: {suggestion_type}")
            return []  # Optionally, raise an exception instead if this is critical.

        return self.driver.find_elements(*locator)

    def click_on_suggestion(self, text, suggestions, search_type):
        chosenProductName = ""

        try:
            # Try to execute the main logic
            if not suggestions:
                raise ValueError("No suggestions found. Retrying...")  # Force retry if list is empty

            # Choose a random element from the suggestions
            chosen_element = random.choice(suggestions)

            # Scroll the element into view
            self.scroll_into_view(chosen_element)

            # Re-locate the element in case the reference is stale
            suggestions = self.get_locator_value(search_type)  # Re-fetch the suggestions
            chosen_element = random.choice(suggestions)  # Re-select the element
            chosenProductName = chosen_element.get_attribute("aria-label")

            # Wait until it's clickable
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(chosen_element))

            # Forcefully click using JavaScript Executor
            self.driver.execute_script("arguments[0].click();", chosen_element)

            print(f"Chosen product: {chosenProductName}")

        except Exception as e:
            print(f"Error: {e}")
            print("Retrying the process...")

            self.enter_text_one_by_one(HomePageLocators.SEARCH_BOX, text)
            print("Executing search function...")  # Debugging

            # Adjusting wait to make sure elements are visible
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_all_elements_located(HomePageLocators.ANIMATED_DIVS)
            )
            # Re-fetch suggestions and retry
            suggestions = self.get_locator_value(search_type)  # Try fetching suggestions again
            if suggestions:
                return self.click_on_suggestion(text, suggestions, search_type)  # Recursively retry

        return chosenProductName