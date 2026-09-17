import pytest
from pages.login_page_forget_password import ForgetPassword
from selenium.common.exceptions import TimeoutException
from utils.screenshot_helper import take_screenshot
from utils.api_helper import api_forget_password
from loguru import logger
import allure

@allure.epic(f"忘記密碼功能")
@allure.feature("測試忘記密碼彈窗")
# @pytest.mark.nondestructive
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_forget_password(driver, base_url, site):
    allure.dynamic.parameter("site", site)
    page = ForgetPassword(driver, base_url)
    page.open()

    with allure.step("檢查忘記密碼彈窗功能"):
        take_screenshot(driver, "確認忘記碼彈窗")
        try:
            result = page.forget_password_check(site)
            if result == True:
                # logger.info(f"[{site}] 忘記密碼彈窗正常")
                assert True
            elif result == "no_data":
                pytest.skip("沒有忘記密碼功能，自動略過此測試")
            else:
                logger.error(f"[{site}] 沒有忘記密碼功能")
                assert False
        except TimeoutException:
            take_screenshot(driver, "忘記密碼未顯示")
            pytest.fail(f"[{site}] 按下忘記密碼後未顯示彈窗")

@allure.epic(f"忘記密碼功能")
@allure.feature("測試忘記密碼API")
# @pytest.mark.nondestructive
def test_forget_password_api(base_url, site):
    with allure.step("檢查忘記密碼api功能"):
        result = api_forget_password(base_url)
        if result:
            logger.info(f"[{site}] 忘記密碼API正常")
            assert True
        else:
            logger.error(f"[{site}] 忘記密碼API異常請確認 | {result[1]}")
            assert False