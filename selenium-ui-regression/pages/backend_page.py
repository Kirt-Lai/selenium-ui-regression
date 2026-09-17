import math
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from loguru import logger


class BackendAnnoPage:
    _FORM_INPUT = (By.CLASS_NAME, "form-control")
    _LOGIN_BTN  = (By.CLASS_NAME, "btn.btn-primary.btn-block")
    _TOTAL_LABEL = (By.CLASS_NAME, "float-right")
    _ACTIVE_BADGE = (By.CLASS_NAME, "badge.badge-success.bulletin-status-badge")

    def __init__(self, driver, base_url):
        self.driver = driver
        self.backend_url = f"https://admin.{base_url}"
        self.wait = WebDriverWait(driver, 10)

    def open_in_new_tab(self):
        logger.info(f"🔗 Opening backend: {self.backend_url}")
        self.driver.execute_script(
            f"window.open('{self.backend_url}', '_blank');"
        )
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def login(self, account, password):
        logger.info(f"👤 Backend login: {account}")
        self.wait.until(EC.presence_of_element_located(self._FORM_INPUT))
        inputs = self.driver.find_elements(*self._FORM_INPUT)
        inputs[0].send_keys(account)
        inputs[1].send_keys(password)
        self.driver.find_element(*self._LOGIN_BTN).click()
        time.sleep(2)

    def get_announcement_count(self):
        """取得後台啟用中公告數量（自動處理分頁）"""
        self.driver.get(
            f"{self.backend_url}/zh-Hant/front/bulletin?per_page=50&page=1"
        )
        self.wait.until(EC.presence_of_element_located(self._TOTAL_LABEL))

        # 從「總筆數 : N」文字取出總數
        label_texts = [
            el.text for el in self.driver.find_elements(*self._TOTAL_LABEL)
            if el.text.strip()
        ]
        total = int(label_texts[0].split(" : ")[1])
        logger.info(f"後台公告總筆數: {total}")

        if total > 50:
            page_count = math.ceil(total / 50)
            count = 0
            for page in range(1, page_count + 1):
                self.driver.get(
                    f"{self.backend_url}/zh-Hant/front/bulletin?per_page=50&page={page}"
                )
                count += len(self.driver.find_elements(*self._ACTIVE_BADGE))
        else:
            count = len(self.driver.find_elements(*self._ACTIVE_BADGE))

        logger.info(f"後台啟用中公告數: {count}")
        return count

    def close_tab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
