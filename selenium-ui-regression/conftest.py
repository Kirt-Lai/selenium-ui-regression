import pytest
from selenium import webdriver
from loguru import logger
from utils.logger import setup_logger
from allure_commons.types import AttachmentType
from utils.api_helper import api_get_user_id
from PIL import Image, ImageChops
from dotenv import load_dotenv
from utils.common import close_anno
from pages.announcement_page import ANNOPAGE
from pages.activity_page import ActivityPage
import allure
import shutil
import os
import tempfile
# import google.generativeai as genai

# 載入 .env 變數
load_dotenv()


# ==========================================
# 1. Gemini AI 初始化 (加入自動修正邏輯)
# ==========================================
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# model = None

# if GEMINI_API_KEY:
#     try:
#         genai.configure(api_key=GEMINI_API_KEY)
#         # 嘗試最標準的名稱
#         model = genai.GenerativeModel('models/gemini-2.5-flash')
#         print("\n💡 [System] Gemini AI 初始化成功！")
#     except Exception as e:
#         print(f"\n❌ [System] Gemini 初始化失敗: {e}")
# else:
#     print("\n⚠️ [System] 找不到 GEMINI_API_KEY 環境變數，AI 分析已停用。")
    
URLDICT = {
    "cu": "cu.demo-platform.example.com",
    "cx": "cx.demo-platform.example.com",
    "db": "db.demo-platform.example.com",
    "dh": "dh.demo-platform.example.com",
    "dk": "dk.demo-platform.example.com",
    "dn": "dn.demo-platform.example.com",
    "dq": "dq.demo-platform.example.com",
    "ds": "ds.demo-platform.example.com",
    "ee": "ee.demo-platform.example.com",
    "eg": "eg.demo-platform.example.com",
    "eh": "eh.demo-platform.example.com",
    "ek": "ek.demo-platform.example.com",
    "el": "el.demo-platform.example.com",
    "en": "en.demo-platform.example.com",
    "ep": "ep.demo-platform.example.com",
    "et": "et.demo-platform.example.com",
    "eu": "eu.demo-platform.example.com",
    "ew": "ew.demo-platform.example.com",
    "ex": "ex.demo-platform.example.com",
    "ey": "ey.demo-platform.example.com",
    "ez": "ez.demo-platform.example.com",
    "fa": "fa.demo-platform.example.com",
    "fb": "fb.demo-platform.example.com",
    "fc": "fc.demo-platform.example.com",
    "demo": "demo-platform.example.com",
}

STATE_NAME = {key: f"Site {key.upper()}" for key in URLDICT}

@pytest.fixture(scope="session", autouse=True)
def configure_logger():
    setup_logger()


@pytest.fixture(
    params=[
        ("pc", "chrome"),
        # ("pc", "firefox"),
        ("mobile", "chrome"),
        # ("mobile", "safari")  # safari 手機版模擬（需要 mac + Safari driver）
    ],
    ids=["pc-chrome", "mobile-chrome"],
)
def driver(request):
    """多裝置、多瀏覽器測試主 Fixture"""
    driver = None
    tmp_dir = None
    device_type, browser_name = request.param
    print(f"當前測試 {device_type} | {browser_name}")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()

        # 👉 每個測試唯一 tmp_dir
        tmp_dir = tempfile.mkdtemp(prefix=f"chrome_userdata_{os.getpid()}_")
        options.add_argument(f"--user-data-dir={tmp_dir}")

        # 👉 適配 CI / Docker
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")

        driver = webdriver.Chrome(options=options)
        driver.set_window_position(1920, 0)  # 0
        if device_type == "pc":
            driver.set_window_size(1920, 1080)
        else:
            driver.set_window_size(430, 932)
        driver.execute_script("document.body.style.zoom='100%'")

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1920, 1080)
        driver.execute_script("document.body.style.zoom='100%'")

    else:
        raise ValueError("Unsupported browser")

    logger.info(f"🚀 Launching {browser_name}")
    yield driver

    # --- teardown ---
    try:
        driver.quit()
        logger.info(f"🧹 {browser_name} closed")
    finally:
        if tmp_dir and os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir, ignore_errors=True)
            logger.info(f"🧹 Removed tmp_dir {tmp_dir}")



# ==========================================
# 2. ListModels + 智能 fallback
# ==========================================
# def get_available_models():
#     """取得支援 generateContent 的可用模型"""
#     url = f"https://generativelanguage.googleapis.com/v1/models?key={GEMINI_API_KEY}"
#     try:
#         resp = requests.get(url)
#         resp.raise_for_status()
#         data = resp.json()
#         models = [m["name"] for m in data.get("models", [])
#         if "generateContent" in m.get("supportedGenerationMethods", [])]
#         return models
#     except Exception as e:
#         print(f"[Model List Error] {e}")
#         return []


# def call_gemini_smart(image_bytes, prompt_text):
#     """自動 fallback：依序嘗試可用模型直到成功"""
#     available_models = get_available_models()
#     if not available_models:
#         print("[AI] 沒有可用模型")
#         return "AI 分析失敗"

#     for model_name in available_models:
#         try:
#             print(f"[AI] 嘗試使用模型: {model_name}")
#             response = genai.GenerativeModel(model_name).generate_content([
#                 {"parts": [
#                     {"mime_type": "image/png", "data": image_bytes},
#                     {"text": prompt_text}
#                 ]}
#             ])
#             return response.text
#         except Exception as e:
#             print(f"[AI] 模型 {model_name} 失敗: {e}")
#             continue

#     return "AI 分析失敗"


# ==========================================
# 3. 圖片比對
# ==========================================
def compare_reference_image(screenshot_path, reference_path):
    """回傳截圖與 reference image 的差異百分比"""
    try:
        img1 = Image.open(screenshot_path).convert("RGB")
        img2 = Image.open(reference_path).convert("RGB")
        diff = ImageChops.difference(img1, img2)
        diff_ratio = sum(diff.getbbox() or [0]) / (img1.width * img1.height)
        return diff_ratio
    except Exception as e:
        print(f"[Image Compare Error] {e}")
        return None


# ==========================================
# 4. AI 結果解析
# ==========================================
# def parse_ai_result(ai_text):
#     """解析 Gemini AI 回傳多行 Root Cause 與 Fix Suggestion"""
#     root_cause, fix_suggestion = "", ""

#     # 抓 Root Cause
#     rc_match = re.search(r"(?i)Root Cause\s*[:\-\s]*\n?(.*?)(?=\n###|\Z)", ai_text, re.S)
#     if rc_match:
#         root_cause = rc_match.group(1).strip()

#     # 抓 Fix Suggestion
#     fix_match = re.search(r"(?i)Fix(?: Suggestion)?\s*[:\-\s]*\n?(.*?)(?=\n###|\Z)", ai_text, re.S)
#     if fix_match:
#         fix_suggestion = fix_match.group(1).strip()

#     fail_type = root_cause or "Unknown Failure"
#     assert_msg = f"{fail_type}. 建議修復: {fix_suggestion}"

#     return fail_type, assert_msg


# ==========================================
# 5. Telegram 通知
# ==========================================
from utils.TG_sendMessage import Bot_sendMessage


# ==========================================
# 6. Gemini 分析整合函式
# ==========================================
# def analyze_failure_with_gemini(item, call, screenshot_path, reference_path=None, site_val="unknown"):
#     print("[AI] 啟動 Gemini 智能分析流程...")

#     # 讀截圖
#     with open(screenshot_path, "rb") as f:
#         img_data = f.read()

#     error_type = call.excinfo.type.__name__
#     error_msg = str(call.excinfo.value)
#     error_trace = str(call.excinfo.getrepr(style="short"))[-1000:]

#     prompt = f"""
#     你是資深 QA 自動化專家。請針對以下失敗案例提供「極簡短」的分析。

#     ## 規則：
#     1. **限 150 字內**。不准有廢話、不准前言與結語。
#     2. **Root Cause**: 僅描述最核心的一個技術原因。
#     3. **Fix**: 列出 2-3 個「關鍵動作」點。
#     4. **格式**: 保持精確，適合手機閱讀。

#     ---
#     案例: {item.name}
#     環境: {site_val}
#     錯誤: {error_type}
#     訊息: {error_msg}
#     堆疊: {error_trace}
#     """

#     # 呼叫 AI
#     ai_report = call_gemini_smart(img_data, prompt)

#     # 解析結果
#     fail_type, assert_msg = parse_ai_result(ai_report)

#     # Allure 報告
#     allure.attach(ai_report, name="🤖 AI Analysis", attachment_type=AttachmentType.TEXT)

#     # Telegram 通知
#     try:
#         from utils.TG_sendMessage import Bot_sendMessage
#         # Bot_sendMessage(f"測試失敗: {item.name}\n{assert_msg}l")
#     except Exception:
#         print("[TG] Telegram 通知失敗，跳過")

#     # pytest assert
#     assert False, assert_msg


# ==========================================
# 7. Pytest Hook
# ==========================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and (rep.failed or rep.outcome == "error"):
        driver = item.funcargs.get("driver") or item.funcargs.get("page")
        if driver:
            os.makedirs("screenshots", exist_ok=True)

            # 取得 --site 參數
            site = item.config.getoption("site") or "unknown"

            # pytest 原生 param，包含 [driver1-tester03-tester03]
            pytest_param = item.name  # ex: test_login[driver1-tester03-tester03]
            print(pytest_param)

            # 拆掉函數名，保留 param
            if "[" in pytest_param:
                func_name = pytest_param.split("[")[0]
                param_part = pytest_param[len(func_name):]  # [driver1-tester03-tester03]
            else:
                func_name = pytest_param
                param_part = ""
            print("paramPart: ", param_part)
            print("func_name: ", func_name)
            print("site:", site)

            # 最終檔名：函數名 + [[site]-param_part].png
            screenshot_name = f"[{site}]_{func_name}{param_part}.png"  # param_part[1:] 去掉原本開頭 [
            print("screenshotName:", screenshot_name)
            screenshot_path = os.path.join("screenshots", screenshot_name)

            # 截圖
            try:
                if hasattr(driver, "save_screenshot"):
                    driver.save_screenshot(screenshot_path)
                else:
                    driver.screenshot(path=screenshot_path)

                allure.attach.file(screenshot_path, name="Failure_Screenshot", attachment_type=AttachmentType.PNG)

            except Exception as e:
                print(f"❌ 截圖失敗: {e}")

            # --- 呼叫 Gemini AI 分析 ---
            # try:
            #     if driver and GEMINI_API_KEY:
            #         analyze_failure_with_gemini(
            #             item=item,
            #             call=call,
            #             screenshot_path=screenshot_path,
            #             reference_path=None,
            #             site_val=site
            #         )
            #     else:
            #         print("⚠️ Gemini AI 未初始化或 driver 不存在，跳過 AI 分析")
            # except AssertionError as ae:
            #     # analyze_failure_with_gemini 裡有 assert False
            #     print(f"🧠 AI 分析完成，測試標記失敗: {ae}")
            # except Exception as e:
            #     print(f"❌ AI 分析失敗: {e}")

# ---- CLI 參數與環境設定 ----
def pytest_addoption(parser):
    parser.addoption("--site", action="store", help="站台代號（例如 AB, CD）")
    parser.addoption("--sha", action="store", help="前端版號（例如 a1ek123k）")


@pytest.fixture(scope="session")
def site(pytestconfig):
    target_site = pytestconfig.getoption("site") or os.getenv("SITE_CODE")
    if not target_site:
        pytest.skip("❌ 未提供 site code，請使用 --site=xx 或設定 SITE_CODE 環境變數")

    if target_site not in URLDICT:
        pytest.skip(f"❌ 無效站台代號：{target_site}，跳過測試")

    return target_site


@pytest.fixture(scope="session")
def sha(pytestconfig):
    target_sha = pytestconfig.getoption("sha") or os.getenv("SHA")
    if not target_sha:
        pytest.skip("❌ 未提供 sha code，請使用 --sha=xx 或設定 SHA 環境變數")
    return target_sha


@pytest.fixture(scope="session")
def base_url(site):
    print("Check: ", URLDICT[site])
    return URLDICT[site]


@pytest.fixture(scope="session")
def site_name(site):
    return STATE_NAME[site]


@pytest.fixture(scope="session")
def user_id(account, password, base_url):
    user_id = api_get_user_id(account, password, base_url)
    assert user_id is not None, "❌ 無法取得 user_id，終止測試"
    return user_id


@pytest.fixture(scope="session")
def account():
    user_account = os.getenv("TEST_ACCOUNT")
    if not user_account:
        pytest.skip("❌ 未設定測試帳號，請設定 TEST_ACCOUNT 環境變數")
    return user_account


@pytest.fixture(scope="session")
def password():
    user_password = os.getenv("TEST_PASSWORD")
    if not user_password:
        pytest.skip("❌ 未設定測試密碼，請設定 TEST_PASSWORD 環境變數")
    return user_password


# Case 判斷 Skip區塊 #
@pytest.fixture
def announcement_available(request, driver, base_url):
    """
    公告前置條件（cached）
    - 僅第一次跑 Selenium 判斷是否有公告
    - 結果寫入 pytest cache
    - 後續 test 直接用 cache 決定 skip
    """
    cache_key = "precondition/announcement_available"
    cached = request.config.cache.get(cache_key, None)

    # 👉 如果已經判斷過，直接用結果
    if cached is False:
        pytest.skip("【cached】沒有公告，跳過公告相關測試")

    if cached is True:
        # 已確認有公告，但仍需 page 給 test 用
        page = ANNOPAGE(driver, base_url)
        page.open()
        return page

    # 👉 第一次才真的跑 Selenium
    page = ANNOPAGE(driver, base_url)
    page.open()
    page.login(os.getenv('TEST_ACCOUNT', 'tester'), os.getenv('TEST_PASSWORD', ''))
    page.go_to_announcement_page(base_url)
    close_anno(driver)

    has_anno = page.check_announcement_num()
    request.config.cache.set(cache_key, has_anno)

    if not has_anno:
        pytest.skip("沒有公告，跳過公告相關測試")

    return page


# ===============================
# Activity precondition
# ===============================
@pytest.fixture
def announcement_available(driver, base_url):
    """
    公告前置條件 fixture
    - 登入
    - 進公告頁
    - 沒公告 -> skip
    """
    page = ANNOPAGE(driver, base_url)
    page.open()
    page.login(os.getenv('TEST_ACCOUNT', 'tester'), os.getenv('TEST_PASSWORD', ''))
    page.go_to_announcement_page(base_url)
    close_anno(driver)


    # print("看一下這裡回傳啥 anno: ", page.check_announcement_num())
    if page.check_announcement_num():
        pytest.skip("沒有公告，跳過公告相關測試")

    return page


# Case 判斷 Skip區塊 #
@pytest.fixture
def activity_available(driver, base_url):
    """
    公告前置條件 fixture
    - 登入
    - 進公告頁
    - 沒公告 -> skip
    """
    page = ActivityPage(driver, base_url)
    page.open()
    page.login(os.getenv('TEST_ACCOUNT', 'tester'), os.getenv('TEST_PASSWORD', ''))
    page.go_to_activityPage(base_url)

    # print("看一下這裡回傳啥 act: ", page.check_activity_num())
    if page.check_activity_num():
        pytest.skip("沒有公告，跳過公告相關測試")

    return page


# ==========================================
# 前後台比對共用 Fixtures
# ==========================================
@pytest.fixture(scope="session")
def token(account, password, base_url):
    from utils.api_helper import api_get_token
    t = api_get_token(account, password, base_url)
    assert t, "❌ 無法取得前台 token，請確認帳號密碼與站台設定"
    return t


@pytest.fixture(scope="session")
def backend_account():
    val = os.getenv("BACKEND_ACCOUNT")
    if not val:
        pytest.skip("❌ 未設定後台帳號，請設定 BACKEND_ACCOUNT 環境變數")
    return val


@pytest.fixture(scope="session")
def backend_password():
    val = os.getenv("BACKEND_PASSWORD")
    if not val:
        pytest.skip("❌ 未設定後台密碼，請設定 BACKEND_PASSWORD 環境變數")
    return val