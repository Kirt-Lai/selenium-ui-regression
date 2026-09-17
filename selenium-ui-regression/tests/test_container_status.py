import time
import pytest
import allure
from loguru import logger
from pages.home_page_check_container import ContainerPage
from utils.common import close_anno


ROTATION_TIMEOUT = 5  # 最多等待幾秒讓輪播圖切換


@allure.epic("首頁輪播圖")
@allure.feature("輪播圖正常輪換確認")
def test_container_status(driver, site, base_url):
    """確認首頁輪播圖是否在 5 秒內自動切換"""
    allure.dynamic.parameter("site", site)

    page = ContainerPage(driver, base_url)

    with allure.step("開啟首頁並關閉公告"):
        page.open()
        close_anno(driver)

    with allure.step("確認輪播圖元件數量"):
        count = page.get_banner_count()
        logger.info(f"[{site}] 輪播圖數量: {count}")

        if count == 0:
            pytest.skip(f"[{site}] 未設定輪播圖，略過測試")
        if count == 1:
            pytest.skip(f"[{site}] 輪播圖僅一張，無須確認輪換")

    with allure.step(f"等待輪播圖在 {ROTATION_TIMEOUT} 秒內切換"):
        initial = page.get_banner_styles()
        start = time.time()
        changed = False

        while time.time() - start < ROTATION_TIMEOUT:
            if page.get_banner_styles() != initial:
                changed = True
                break
            time.sleep(0.3)

        logger.info(f"[{site}] 輪播圖{'有' if changed else '未'}切換")
        assert changed, f"[{site}] 輪播圖在 {ROTATION_TIMEOUT} 秒內未自動切換"
