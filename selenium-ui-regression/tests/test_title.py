import pytest
from pages.home_page_check_title import TitleCheck
from utils.screenshot_helper import take_screenshot
from selenium.common.exceptions import TimeoutException
from loguru import logger
import allure

@allure.epic("檢查標題是否符合")
# @pytest.mark.nondestructive
def test_title(driver, site, base_url , site_name):
    allure.dynamic.parameter("site", site)
    page = TitleCheck(driver, base_url)
    page.open()

    with allure.step("檢查標題"):
        title = page.check_title()
        assert site_name in title , f"[{site}] Title is Fail"