import os
from pathlib import Path
from loguru import logger

def setup_logger():
    # 先從環境變數 LOG_DIR 讀取，沒有就 fallback 到 /tmp/logs
    log_dir = Path(os.getenv("LOG_DIR", "/tmp/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "test_{time:YYYY-MM-DD}.log",
        rotation="1 day",        # 每天新檔
        retention="7 days",      # 保留 7 天
        level="INFO",
        encoding="utf-8"
    )
    return logger