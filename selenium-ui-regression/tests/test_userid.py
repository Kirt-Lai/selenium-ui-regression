import pytest
# from pages.get_userid import UserID
from utils.screenshot_helper import take_screenshot
import allure

@allure.epic("測試取user_id的api")
# @pytest.mark.nondestructive
def test_user_id_available(user_id):
    """
    驗證是否成功透過 API 登入並取得 user_id。
    (直接從conftest call back, page底下無對應code)
    """
    assert user_id, "❌ 未成功取得 user_id，請確認帳號密碼或 API 是否正常"
    # print(f"✅ 成功取得 user_id：{user_id}")