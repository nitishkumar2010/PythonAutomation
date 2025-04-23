from selenium.webdriver.common.by import By

class HomePageLocators:
    SEARCH_BOX = (By.XPATH, ".//div/input[@id='mastheadSeachBox']")
    ANIMATED_DIVS = (By.XPATH, "(.//div[contains(@class,'aos-animate')])[2]")
    FIND_YOUR_DREAM_HOME_BUTTON = (By.ID, "Find Your Dream Home")
    PREFETCH_BUTTONS = (By.XPATH, ".//button[@rel='prefetch']")
    COMMUNITY_SUGGESTIONS = (By.XPATH, ".//p[text()='Communities']/../..//a[@href]")
    QMI_SUGGESTIONS = (By.XPATH, ".//p[text()='Quick Move-Ins']/../..//a[@href]")
    PLAN_SUGGESTIONS = (By.XPATH, ".//p[text()='Plans']/../..//a[@href]")
    MARKET_SUGGESTIONS = (By.XPATH, ".//p[text()='Market']/../..//a[@href]")


class SearchResultsLocators:
    REDIRECTION_METRO_NAME = (By.XPATH, "(.//section[@id='MetroSearch']//div[contains(@aria-label,'Results will filter on the page')]/div/span)[1]")
    COMMUNITY_CARD_PRICES = (By.XPATH, ".//*[@id='ProductInfo']//div[text()='Starting From']/../span[not(ancestor::div[contains(@class, 'aos-animate')] and ancestor::div[contains(@class, 'bg-light-blue')])]")
    MPC_CARDS = (By.XPATH, "(.//div[contains(@class,'aos-animate')]//div[contains(@class,'bg-light-blue')])")
    MPC_CARD_PRICE = lambda index: (By.XPATH, f"({SearchResultsLocators.MPC_CARDS[1]})[{index + 1}]//div[@id='ProductInfo']//div[text()='Starting From']/../span")
    MPC_CARD_COMMUNITY_NAME = lambda index: (By.XPATH, f"({SearchResultsLocators.MPC_CARDS[1]})[{index + 1}]//div[contains(@class,'text-3xl')]")
    SORT_DROPDOWN = (By.XPATH, ".//div[contains(@aria-label,'selector')]//button[contains(@aria-label,'dropdown')]")
    SORT_OPTIONS = (By.XPATH, ".//div[contains(@aria-label,'selector')]/..//button/span")
    PLAN_CARD_PRICES = (By.XPATH, ".//div[contains(text(),'Starting From')]/../span/span[1]")
    QMI_CARD_PRICES = (By.XPATH, ".//div[@id='ProductInfo']//a/span/span[1]")
    QMI_TAB = (By.XPATH, ".//section[@id='MetroSearch']//div[contains(@class,'blue-light')]//div[contains(@class,'items')]/div[3]")
    PLAN_TAB = (By.XPATH, ".//section[@id='MetroSearch']//div[contains(@class,'blue-light')]//div[contains(@class,'items')]/div[4]")