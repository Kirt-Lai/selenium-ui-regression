import pytest
from pages.login_page_shacheck import SHACHECK
from utils.screenshot_helper import take_screenshot
from selenium.common.exceptions import TimeoutException
from loguru import logger
import allure

@allure.epic("前端版號確認")
# @pytest.mark.nondestructive
def test_frond_version(driver, site, base_url, pytestconfig):
    """確認前端版本是否正確"""
    page = SHACHECK(driver, base_url)
    page.open()

    sha = pytestconfig.getoption("sha")
    allure.dynamic.label("site", site)
    with allure.step("取得 SHA 版本"):
        actual_sha = page.get_sha_version()
    with allure.step("驗證 SHA 版本是否正確"):
        assert actual_sha == sha, f"[{site}] SHA 錯誤，預期：{sha}，實際：{actual_sha}"
        logger.info("SHA 版本正確")