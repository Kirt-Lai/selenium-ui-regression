from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from loguru import logger
# from base_page import BasePage
from .wait import wait_for_element, wait_until_clickable
import time

def close_anno(driver):
    """關閉重要公告、彈窗公告"""
    # 初始化Action
    actions = ActionChains(driver)

    try:
        if driver.find_element(By.CLASS_NAME, "v-input--selection-controls__input"):
            anno1 = True
    except NoSuchElementException:
        anno1 = False

    try:
        if driver.find_element(By.CLASS_NAME, 'pop-pic'):
            anno2 = True
    except NoSuchElementException:
        anno2 = False
    # print("看一下判斷:", anno1, anno2)
    if anno1 and anno2:
        try:
            # wait_until_clickable(driver, By.CLASS_NAME, "v-input--selection-controls__input")
            # e = driver.find_element(By.CLASS_NAME, "v-input--selection-controls__input")
            # driver.execute_script("arguments[0].click();", e)
            actions.move_by_offset(10, 10).click().perform()
            time.sleep(0.5)
            actions.move_by_offset(10, 10).click().perform()
        except:
            actions.move_by_offset(10, 10).click().perform()
            # wait_until_clickable(driver, By.CLASS_NAME, "v-input--selection-controls__input")
            # wait_for_element(By.CLASS_NAME, "v-input--selection-controls__input")
            # e = driver.find_element(By.CLASS_NAME, "v-input--selection-controls__input")
            # driver.execute_script("arguments[0].click();", e)
            time.sleep(0.5)
            actions.move_by_offset(10, 10).click().perform()
    elif anno1 == True and not anno2:
        # wait_until_clickable(driver, By.CLASS_NAME, "v-input--selection-controls__input")
        # wait_for_element(By.CLASS_NAME, "v-input--selection-controls__input")
        # e = driver.find_element(By.CLASS_NAME, "v-input--selection-controls__input")
        # driver.execute_script("arguments[0].click();", e)
        time.sleep(0.5)
        actions.move_by_offset(10, 10).click().perform()
    elif not anno1 and anno2 == True:
        actions.move_by_offset(10, 10).click().perform()
    else:
        pass
    return anno1, anno2
