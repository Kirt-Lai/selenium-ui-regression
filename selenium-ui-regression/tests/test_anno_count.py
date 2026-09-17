import pytest
import allure
from loguru import logger
from pages.backend_page import BackendAnnoPage
from utils.api_helper import api_get_bulletin_count

ANNOUNCEMENT_PATH = "/lobby/announcement"


@allure.epic("公告管理")
@allure.feature("前後台公告數量比對")
def test_anno_count(driver, site, base_url, token, backend_account, backend_password):
    """確認前台 API 公告數量與後台啟用中公告數量一致"""
    allure.dynamic.parameter("site", site)

    with allure.step("確認前台公告頁存在"):
        driver.get(f"https://{base_url}{ANNOUNCEMENT_PATH}")
        if ANNOUNCEMENT_PATH not in driver.current_url:
            pytest.skip(f"[{site}] 此站台無公告頁面，略過")

    with allure.step("取得前台公告數量（API）"):
        front_count = api_get_bulletin_count(token, base_url)
        assert front_count is not None, f"[{site}] 無法取得前台公告數量，請確認 token 與 API"
        logger.info(f"[{site}] 前台公告數: {front_count}")

    with allure.step("取得後台啟用中公告數量"):
        backend = BackendAnnoPage(driver, base_url)
        backend.open_in_new_tab()
        backend.login(backend_account, backend_password)
        back_count = backend.get_announcement_count()
        backend.close_tab()
        logger.info(f"[{site}] 後台公告數: {back_count}")

    with allure.step("比對前後台公告數量"):
        assert front_count == back_count, (
            f"[{site}] 前後台公告數量不符：前台 {front_count} 筆，後台啟用 {back_count} 筆"
        )
