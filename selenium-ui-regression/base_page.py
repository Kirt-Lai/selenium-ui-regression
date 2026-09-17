from selenium.webdriver.common.by import By
from utils.wait import wait_for_element, wait_until_clickable
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def _unlock_vuetify_overlay(self):
        self.driver.execute_script("""
        // 只解鎖互動，不移除 DOM（避免 Vue state 壞掉）
        document.body.classList.remove('overflow-hidden');
        document.body.style.overflow = 'auto';
        document.body.style.pointerEvents = 'auto';

        document.querySelectorAll('.UiDialogAxiosOverlay, .v-overlay').forEach(el => {
            el.style.pointerEvents = 'none';
            el.style.background = 'transparent';
        });
        """)

    def click(self, by, value, index=None):
        self._unlock_vuetify_overlay()

        try:
            if index is not None:
                elems = self.driver.find_elements(by, value)
                wait_until_clickable(self.driver, by, value)
                # print("check: ", elems[index].text)
            else:
                elem = wait_until_clickable(self.driver, by, value)
                elem.click()
        except ElementClickInterceptedException:
            self._unlock_vuetify_overlay()
            if index is not None:
                self.driver.execute_script("arguments[0].click();", elems[index])
            else:
                self.driver.execute_script("arguments[0].click();", elem)

    def input_text(self, by, value, text, index=None):
        self._unlock_vuetify_overlay()

        if index == "text":
            pass
        elif index is not None:
            elems = self.driver.find_elements(by, value)
            wait_for_element(self.driver, by, value)
            elem = elems[index]
        else:
            elem = wait_for_element(self.driver, by, value)

        elem.clear()
        elem.send_keys(text)

    def find(self, by, value):
        self._unlock_vuetify_overlay()
        return wait_for_element(self.driver, by, value)

    def finds(self, by, value):
        """回傳一組符合條件的元素 list"""
        self._unlock_vuetify_overlay()
        return self.driver.find_elements(by, value)

    def get_text(self, by, value):
        self._unlock_vuetify_overlay()
        return self.find(by, value).text
    
    def page_contains_text(self, text, timeout=5):
        """回傳頁面上是否包含特定文字（帶有等待機制）"""
        # 使用 XPath 尋找包含該文字的任何元素
        xpath = f"//*[contains(text(), '{text}')]"
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            # 超時後再做最後一次全頁比對，確保萬無一失
            return text in self.driver.page_source