import pytest
from utils.screenshot_helper import take_screenshot
from pages.announcement_page import ANNOPAGE
from loguru import logger
import allure

@allure.epic(f"最新公告功能測試")
@allure.feature("最新公告頁面 & 標題是否正常")
# @pytest.mark.nondestructive
def test_announcement_loads(driver, base_url, announcement_available):
    # page = ANNOPAGE(driver, base_url)
    # page.open()
    page = announcement_available

    with allure.step("登入帳號後切換到最新公告頁，並確認活動標題是否顯示"):
        # page.login("tester03", "tester03")
        # page.go_to_announcementPage(base_url)
        # page.wait_card_title()
        items = page.get_title()
        assert len(items) > 0, "活動標題無正常顯示"
        

@allure.feature("最新公告彈窗 & 彈窗內內容是否正確")
# @pytest.mark.nondestructive
def test_announcement_newpage(driver, base_url, announcement_available):
    # page = ANNOPAGE(driver, base_url)
    # page.open()
    page = announcement_available

    with allure.step("登入帳號後切換到最新公告頁，開啟彈窗後確認活動標題是否顯示"):
        # page.login("tester03", "tester03")
        # page.go_to_announcementPage(base_url)
        page.click_first_announcement()
        page.check_title_after_click()
        items = page.get_after_title()
        assert len(items) > 0, "活動點擊沒反應 or 開啟彈窗後沒標題"