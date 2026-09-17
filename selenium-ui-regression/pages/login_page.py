from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from base_page import BasePage
from loguru import logger
import time

class LoginPage(BasePage):
    def __init__(self, driver, base_url):
        self.driver = driver
        # print(base_url)
        self.url = f"https://{base_url}/auth/login"
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(driver)

    def open(self):
        logger.info("🔗 Opening login page")
        print(self.url)
        self.driver.get(self.url)

    def login(self, account, password):
        logger.info(f"👤 Logging in with {account}")
        # 測試錯誤情境
        # self.input_text(By.ID, "button", account, 0)
        self.input_text(By.CSS_SELECTOR, "input", account, 0)
        self.input_text(By.CSS_SELECTOR, "input", password, 1)
        # 尋找登入按鈕後按下
        [ n.click() for n in self.finds(By.TAG_NAME, "button") if n.text == "登入" ]
        try:
            self.wait.until_not(EC.url_contains("/auth/login/"))
            return True
        except TimeoutException:
            return False