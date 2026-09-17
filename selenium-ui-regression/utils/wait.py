from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

def wait_for_element(driver, by, value, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def wait_until_clickable(driver, by, value, timeout=DEFAULT_TIMEOUT):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))

def wait_for_visible_text_disappear(driver, text, timeout=10):
    """等待頁面上可見文字消失"""
    xpath = f"//*[contains(text(), '{text}')]"
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, xpath))
        )
        return True
    except:
        return False