import pytest
import allure
from loguru import logger
from pages.game_page import GamePage
from utils.common import close_anno


GAME_CATEGORIES = [
    ("熱門", "/games?category=hots"),
    ("體育", "/games?category=sport"),
    ("電子", "/games?category=e-game"),
    ("真人", "/games?category=live"),
    ("彩票", "/games?category=keno"),
    ("棋牌", "/games?category=e-battle"),
    ("捕魚", "/games?category=fishing"),
]


@allure.epic("遊戲館圖片")
@allure.feature("遊戲館圖片正常載入確認")
@pytest.mark.parametrize(
    "category_name,category_path",
    GAME_CATEGORIES,
    ids=[path.split("=")[1] for _, path in GAME_CATEGORIES],
)
def test_game_image(driver, site, base_url, category_name, category_path):
    """確認各遊戲館的圖片是否全部正常載入"""
    allure.dynamic.parameter("site", site)
    allure.dynamic.parameter("category", category_name)

    page = GamePage(driver, base_url)

    with allure.step(f"開啟 [{category_name}] 館別頁面"):
        page.open_category(category_path)
        close_anno(driver)

    with allure.step("確認遊戲列表是否存在"):
        if not page.has_games():
            pytest.skip(f"[{site}] {category_name} 館別無遊戲，略過")

    with allure.step("比對遊戲數量與圖片數量"):
        image_num = page.get_image_count()
        game_num = page.get_game_count()
        # image_num - 1 扣除館別 header 圖片
        loaded_images = image_num - 1

        logger.info(
            f"[{site}] {category_name}: 遊戲數={game_num}, 圖片數(扣header)={loaded_images}"
        )

        missing = game_num - loaded_images
        assert loaded_images == game_num, (
            f"[{site}] {category_name} 圖片載入不完整："
            f"共 {game_num} 款遊戲，缺少 {missing} 張圖片"
        )
