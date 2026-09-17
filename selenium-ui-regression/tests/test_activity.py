import pytest
from utils.screenshot_helper import take_screenshot
from pages.activity_page import ActivityPage
from loguru import logger
import allure

@allure.epic(f"優惠活動功能測試")
@allure.feature("優惠活動頁面 & 標題是否正確")
# @pytest.mark.nondestructive
def test_activity_loads(driver, base_url, activity_available):
    # page = ActivityPage(driver, base_url)
    # page.open()
    page = activity_available

    with allure.step("登入帳號後切換到優惠活動頁，並確認活動標題是否顯示"):
        # page.login("tester03", "tester03")
        # page.go_to_activityPage(base_url)
        # page.wait_card_title()
        
        items = page.get_title()
        assert len(items) > 0, "活動標題無正常顯示"
        
@allure.epic(f"優惠活動功能測試")
@allure.feature("優惠活動彈窗 & 標題是否正確")
# @pytest.mark.nondestructive
def test_activity_pop_loads(driver, base_url, activity_available):
    # page = ActivityPage(driver, base_url)
    # page.open()
    page = activity_available

    with allure.step("登入帳號後切換到優惠活動頁，開啟彈窗後確認活動內容是否顯示"):
        # page.login("tester03", "tester03")
        # page.go_to_activityPage(base_url)
        # page.wait_card_title()
        page.click_first_activity()
        page.check_title_after_click()
        items = page.get_after_title()
        assert len(items) > 0, "活動點擊沒反應 or 開啟彈窗後沒內容"