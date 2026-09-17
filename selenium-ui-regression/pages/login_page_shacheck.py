from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from loguru import logger
from base_page import BasePage
import time


class SHACHECK(BasePage):
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}/auth/login"
        # self.wait = WebDriverWait(self.driver, 10)
        # self.actions = ActionChains(driver)
    def open(self):
        logger.info("🔗 Opening login page")
        self.driver.get(self.url)
    def get_sha_version(self):
        """等待並抓取畫面上的 SHA 版本字串"""
        # try:
        #     self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "mt-1")))
        #     sha_text = self.driver.find_element(By.CLASS_NAME, "mt-1").text.replace("SHA:", "")
        #     sha_clean = sha_text.strip()
        #     return sha_clean
        # except TimeoutException:
        #     logger.warning("❌ 未找到 SHA 元素，Timeout")
        #     return None
        try:
            sha_text = self.get_text(By.CLASS_NAME, "mt-1").replace("SHA:", "").strip()
            return sha_text
        except TimeoutException:
            logger.warning("❌ 未找到 SHA 元素，Timeout")
            return None
