from selenium.webdriver.common.by import By
from loguru import logger


class ContainerPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}"

    def open(self):
        logger.info(f"🔗 Opening home page: {self.url}")
        self.driver.get(self.url)

    def get_banner_count(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "v-window-item"))

    def get_banner_styles(self):
        return [
            el.get_attribute("style")
            for el in self.driver.find_elements(By.CLASS_NAME, "v-window-item")
        ]
