from selenium.webdriver.common.by import By
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


def verify_redirection(driver, chosenProductName, xpath, ignore_case=False):
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath))
    )
    product_element = driver.find_element(By.XPATH, xpath)
    actual_name = product_element.text

    print(actual_name)
    print(chosenProductName)

    if ignore_case:
        assert actual_name.upper() == chosenProductName.upper(), "❌ Failed to verify that the redirection happens correctly!"
    else:
        assert actual_name == chosenProductName, "❌ Failed to verify that the redirection happens correctly!"

    print("✅ Verified that the redirection happens correctly")