from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from loguru import logger

class TitleCheck():
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}/auth/login"
        self.wait= WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)

    def open(self):
        logger.info("🔗 Opening login page")
        print(self.url)
        self.driver.get(self.url)

    def check_title(self):
        title = self.driver.title
        return title