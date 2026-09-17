from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from base_page import BasePage
from utils.wait import wait_until_clickable, wait_for_visible_text_disappear
from loguru import logger
import time

class ActivityPage(BasePage):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}/auth/login"
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(driver)

    def open(self):
        logger.info("🔗 Opening login page")
        self.driver.get(self.url)

    def login(self, account, password):
        logger.info(f"👤 Logging in with {account}")
        # Login Process
        self.input_text(By.CSS_SELECTOR, "input", account, 0)
        self.input_text(By.CSS_SELECTOR, "input", password, 1)
        self.click(By.TAG_NAME, "button", 3)

    def go_to_activityPage(self, base_url):
        activity_url = f"https://{base_url}/lobby/activity"
        self.driver.get(activity_url)

    def check_activity_num(self):
        wait_for_visible_text_disappear(self.driver, "讀取中")
        time.sleep(1)
        # print("Check Page: ", self.page_contains_text("尚無任何活動"))
        return self.page_contains_text("尚無任何活動")
        # wait_until_clickable(self.driver, By.CLASS_NAME, "v-card__title")

    def get_title(self):
        title_list = [ n.text for n in self.driver.find_elements(By.CLASS_NAME, "v-card__title") ]
        return title_list

    def click_first_activity(self):
        e = self.find(By.CLASS_NAME, "v-card__title")
        self.actions.move_to_element(e).perform()
        self.driver.execute_script("arguments[0].click();", e)

    def check_title_after_click(self):
        wait_until_clickable(self.driver, By.CLASS_NAME, "v-html")

    def get_after_title(self):
        title_list = [n.text for n in self.driver.find_elements(By.CLASS_NAME, "v-html")]
        return title_list