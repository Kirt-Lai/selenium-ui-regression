# Selenium UI Regression

多站前台 UI 回歸框架。用站台代號切環境，同一套 Page Object 跑登入、忘記密碼、前端版號、頁面標題、公告、活動、遊戲館圖片，以及前後台公告數量比對。

## 測試框架

| 層級 | 套件 | 用途 |
| --- | --- | --- |
| 測試執行 | pytest | 收集／參數化／fixture／CLI `--site` `--sha` |
| UI 自動化 | Selenium WebDriver | Chrome（PC 1920×1080 與手機 430×932） |
| 報告 | allure-pytest | 步驟、失敗截圖、Allure 報告 |
| 重跑 | pytest-rerunfailures | 失敗後重跑 |
| 日誌 | loguru | 測試過程 log |
| API 輔助 | requests | 登入取 token／user id、公告數量 |
| 通知 | python-telegram-bot | 可選，失敗通知（token 走環境變數） |
| CI | Docker + Jenkins | 建 image → 跑 pytest → 產 Allure |

架構是 **Page Object Model**：`base_page.py` 處理 overlay／等待，`pages/` 放頁面操作，`tests/` 只寫流程與 assert。

## 實際作用流程

1. **選站台**  
   `pytest --site=cu --sha=<前端版號>`。`conftest.py` 的 `URLDICT` 把代號對到網域；沒給 `--site` 或代號不存在就 skip。

2. **開瀏覽器**  
   session fixture 依序跑 `pc-chrome`、`mobile-chrome`。每個 case 用獨立 Chrome user-data 目錄，避免 cookie 互相污染。

3. **登入與共用狀態**  
   `TEST_ACCOUNT` / `TEST_PASSWORD` 從 `.env` 讀。需要 user id 或 JWT 時，走 `utils/api_helper.py` 打登入 API，而不是再開一次 UI。

4. **各模組檢查**

   | 測試檔 | 實際在做什麼 |
   | --- | --- |
   | `tests/test_login.py` | 開 `/auth/login` → 填帳密 → 等 URL 離開登入頁 |
   | `tests/test_forget_password.py` | UI 走忘記密碼；另外打 forget-password API 看是否異常 |
   | `tests/test_sha.py` | 登入後核對前端版號是否等於 `--sha` |
   | `tests/test_title.py` | 站台標題是否與設定名稱一致 |
   | `tests/test_announcement.py` | 進公告頁，確認有內容才繼續 |
   | `tests/test_activity.py` | 進活動頁，沒活動就 skip |
   | `tests/test_game_image.py` | 熱門／體育／電子／真人／彩票／棋牌／捕魚各館：遊戲張數要等於圖片張數 |
   | `tests/test_userid.py` | API 拿到的 user id 與前台顯示一致 |
   | `tests/test_anno_count.py` | 前台公告數 vs 後台公告數 |
   | `tests/test_container_status.py` | 首頁區塊／容器是否正常顯示 |

5. **失敗處理**  
   `pytest_runtest_makereport` 失敗時截圖，檔名帶站台與參數，掛到 Allure。可選 Telegram 通知。

6. **CI**  
   Jenkins 參數 `site`、`sha` → Docker 跑 pytest → `allure generate`。

```
pytest --site --sha
        │
        ▼
  Chrome PC / Mobile
        │
        ├─ 登入 / 忘記密碼
        ├─ 版號 SHA、頁面標題
        ├─ 公告、活動、遊戲館圖片
        └─ API user id／前後台公告數
                │
                ▼
         Allure + 失敗截圖
```

## 怎麼跑

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
pytest --site=cu --sha=demo-sha
allure serve allure-results
```

常用篩選：

```bash
pytest tests/test_login.py --site=cu --sha=demo-sha
pytest -k "login or sha" --site=cu --sha=demo-sha
```
