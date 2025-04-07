from selenium.webdriver.common.by import By

class HomePageLocators:
    SEARCH_BOX = (By.XPATH, ".//div/input[@id='mastheadSeachBox']")

class SearchResultsPageLocators:
    PROMO_CLOSE_BTN = (By.XPATH, ".//div[contains(@class,'promo-flex')]/div/button/div")
    SORT_BUTTON = (By.XPATH, "(.//span[contains(text(),'Sort:')]/../button)[1]")
    SORT_OPTIONS = (By.XPATH, ".//div[contains(@class,'dropdown-content')]/li")
    PRICE_LIST = (By.XPATH, ".//div[contains(@class,'car-items-end')]/div[contains(@class,'700')]//div[contains(text(),'$')]")
    ALL_PRICES = (By.XPATH, ".//div[contains(@class,'car-items-end')]/div[contains(@class,'700')]//div[contains(text(),'$')]")