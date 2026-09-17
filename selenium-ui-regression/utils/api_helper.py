import requests
from loguru import logger

# @pytest.mark.nondestructive
def api_get_user_id(account, password, base_url):
    url = f"https://api.{base_url}/api/login?subDomain=www&lang=zh-Hant"
    payload = {
        "last_login_browser": "",
        "last_login_device": "desktop",
        "last_login_system": "",
        "user_identify": account,
        "password": password,
        "captcha": ""
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        user_id = data["result"]["id"]
        return user_id
    except Exception as e:
        from loguru import logger
        logger.exception("登入 API 失敗")
        return None, {"error": str(e)}
    
def api_forget_password(base_url):
    url = f"https://api.{base_url}/api/forget-password?subDomain=www&lang=zh-Hant"
    payload = {
        "username": "test8test",
        "i18n_calling_code": "886",
        "mobile": "0900000000",
        "code": "123321",
        "new_password": "test8test"
    }
    response = requests.post(url, json=payload, timeout=10)
    if response.status_code not in [404, 405, 502]:
        "❌ API 可能掛掉"
        result = True
    else:
        result = False

    return [result, [response.status_code, response.json()]]

def api_member(base_url, token):
    url = f"https://api.{base_url}/api/member?subDomain=www&lang=zh-Hant"
    header = {
        "authorization": "Bearer" + token
    }
    response = requests.get(url, headers=header)
    if response.status_code not in [404, 405, 502]:
        "❌ API 可能掛掉"
        result = True
    else:
        result = False

    return [result, [response.status_code, response.json()]]


def api_get_token(account, password, base_url):
    """取得前台登入 JWT token，回傳含 Bearer 前綴的完整字串"""
    url = f"https://api.{base_url}/api/login?subDomain=www&lang=zh-Hant"
    payload = {
        "last_login_browser": "",
        "last_login_device": "desktop",
        "last_login_system": "",
        "user_identify": account,
        "password": password,
        "captcha": ""
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        token = data["result"]["token"]  # 若 key 不同請依實際 API response 調整
        return f"Bearer {token}"
    except Exception:
        logger.exception("取得 token 失敗")
        return None


def api_get_bulletin_count(token, base_url):
    """取得前台公告總數（需要 Bearer token）"""
    url = (
        f"https://api.{base_url}/api/bulletin/after-login"
        f"?subDomain=www&lang=zh-Hant&page=1&per_page=10"
    )
    try:
        response = requests.get(url, headers={"Authorization": token}, timeout=10)
        response.raise_for_status()
        return int(response.json()["pagination"]["total"])
    except Exception:
        logger.exception("取得前台公告數量失敗")
        return None

