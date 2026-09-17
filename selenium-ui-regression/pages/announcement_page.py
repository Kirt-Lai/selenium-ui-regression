from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from base_page import BasePage
from utils.wait import wait_for_element, wait_for_visible_text_disappear
from utils.common import close_anno
from loguru import logger
import time

class ANNOPAGE(BasePage):
    # 匯入ELEMENT
    LOGIN_INPUT = (By.CSS_SELECTOR, "input")
    CLICK_LOGIN = (By.TAG_NAME, "button")
    CART_TITLE = (By.CLASS_NAME, "v-card__title")
    ANNO_CONTENT = (By.CLASS_NAME, "v-html")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}/auth/login"
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(driver)

    def open(self):
        logger.info("🔗 Opening login page")
        # print(self.url)
        self.driver.get(self.url)

    def login(self, account, password):
        logger.info(f"👤 Logging in with {account}")
        # Login Process
        self.input_text(*self.LOGIN_INPUT, account, 0)
        self.input_text(*self.LOGIN_INPUT, password, 1)
        self.click(*self.CLICK_LOGIN, 3)

    def go_to_announcement_page(self, base_url):
        announcement_url = f"https://{base_url}/lobby/announcement"
        self.driver.get(announcement_url)

    def check_announcement_num(self):
        wait_for_visible_text_disappear(self.driver, "讀取中")
        time.sleep(1)
        return self.page_contains_text("尚無任何公告")

    def get_title(self):
        title_list = [ n.text for n in self.driver.find_elements(*self.CART_TITLE) ]
        return title_list

    def click_first_announcement(self):
        time.sleep(1)
        e = self.find(*self.CART_TITLE)
        self.actions.move_to_element(e).perform()
        self.driver.execute_script("arguments[0].click();", e)

    def check_title_after_click(self):
        wait_for_element(self.driver, *self.ANNO_CONTENT)
        self.driver.execute_script("arguments[0].click();", self.find(*self.ANNO_CONTENT))

    def get_after_title(self):
        title_list = [n.text for n in self.driver.find_elements(*self.ANNO_CONTENT)]
        return title_list