import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from loguru import logger


class GamePage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open_category(self, category_path):
        url = f"https://{self.base_url}{category_path}"
        logger.info(f"🔗 Opening game category: {url}")
        self.driver.get(url)

    def has_games(self):
        """等待遊戲名稱出現，無則回傳 False（該館別未開放）"""
        try:
            self.wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "text-subtitle-1"))
            )
            return True
        except TimeoutException:
            return False

    def get_game_count(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "text-subtitle-1"))

    def get_image_count(self):
        # 等 2 秒讓圖片非同步載入完成
        time.sleep(2)
        return len(
            self.driver.find_elements(
                By.CLASS_NAME, "v-image__image.v-image__image--cover"
            )
        )
