from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_clickable(driver, element):
    """Check if an element is clickable."""
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(element))
        return True
    except:
        return False

def click_first_or_second_element(driver, xpath):
    """
    Clicks the first clickable element if available, otherwise clicks the second.
    """
    elements = driver.find_elements("xpath", xpath)

    if len(elements) > 0 and is_clickable(driver, elements[0]):
        driver.execute_script("arguments[0].click();", elements[0])
        print("Clicked on the first clickable element")
    elif len(elements) > 1 and is_clickable(driver, elements[1]):
        driver.execute_script("arguments[0].click();", elements[1])
        print("First element was not clickable, clicked on the second element")
    else:
        print("No clickable elements found")
