import os
import pytest
from pages.login_page import LoginPage
from utils.screenshot_helper import take_screenshot
import allure

@allure.epic(f"登入功能測試")
# @pytest.mark.nondestructive
@pytest.mark.parametrize("account,password", [
    (os.getenv("TEST_ACCOUNT", "tester"), os.getenv("TEST_PASSWORD", "")),
])
# @pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_login(driver, account, password, base_url, site):
    allure.dynamic.parameter("site", site)
    page = LoginPage(driver, base_url)
    page.open()

    with allure.step("執行登入動作"):
        take_screenshot(driver, "登入前畫面")
        result = page.login(account, password)
        take_screenshot(driver, "登入後畫面")
        assert result, f"{site} 登入功能異常無跳轉"
