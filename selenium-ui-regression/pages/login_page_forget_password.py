from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from loguru import logger
import time

class ForgetPassword:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = f"https://{base_url}/auth/login"
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(driver)

    def open(self):
        logger.info("🔗 Opening login page")
        print(self.url)
        self.driver.get(self.url)

    def forget_password_check(self, site):
        """
        點擊「忘記密碼?」並等待彈窗/頁面元素出現。
        回傳 True = 正常跳出；False = 找不到按鈕；TimeoutException 代表按鈕有點到但畫面沒出來。
        """
        btns =  [n  for i, n in enumerate(self.driver.find_elements(By.CLASS_NAME, "v-btn__content")) if n.text == "忘記密碼?"]
        if not btns:
            return "no_data"
        else:
            btns[0].click()
        try:
            self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "v-card__title")))
            logger.info(f"[{site}]: Forget Password Normal. Correct")
            return True
        except TimeoutError:
            logger.info(f"[{site}]: Forget Password don't show. Fail")
            return False
        