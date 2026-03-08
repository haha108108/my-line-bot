"""環境變數設定管理"""

import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Settings:
    LINE_TOKEN = os.getenv("LINE_TOKEN")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
    LINE_USER_ID = os.getenv("LINE_USER_ID", "")  # 可選：固定發送對象
    TELEGRAM_CHAT_IDS = os.getenv(
        "TELEGRAM_CHAT_IDS",
        ""
    ).split(",")  # 多個 Chat ID 用逗號分隔

    @classmethod
    def validate(cls) -> bool:
        """驗證必要變數是否存在"""
        required = [
            cls.LINE_TOKEN,
            cls.TELEGRAM_TOKEN,
            cls.FB_PAGE_ACCESS_TOKEN,
        ]
        return all(required)

    @classmethod
    def get_printable(cls) -> dict:
        """取得可以用於 Debug 的設定（不含敏感資訊）"""
        return {
            "LINE_TOKEN": "***" if cls.LINE_TOKEN else "MISSING",
            "TELEGRAM_TOKEN": "***" if cls.TELEGRAM_TOKEN else "MISSING",
            "FB_PAGE_ACCESS_TOKEN": "***" if cls.FB_PAGE_ACCESS_TOKEN else "MISSING",
            "LINE_USER_ID": cls.LINE_USER_ID if cls.LINE_USER_ID else "DEFAULT",
            "TELEGRAM_CHAT_IDS": cls.TELEGRAM_CHAT_IDS,
        }
