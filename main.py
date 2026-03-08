#!/usr/bin/env python3
"""
健康內容自動傳送器

功能：
- 統一管理健康內容
- 自動發送到 LINE、Telegram、FB 等平台
"""

import yaml
import requests
import random
from datetime import datetime
import json
import os
from typing import List, Dict

class HealthDistributor:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self._validate_config()

    def _load_config(self) -> Dict:
        """載入設定檔"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"設定檔 config.yaml 不存在。\n"
                f"請複製 config_template.yaml 並改成 config.yaml，然後填入你的資訊。"
            )

    def _validate_config(self):
        """驗證設定"""
        required_fields = {
            'line': ['token', 'profile_id'],
            'telegram': ['token', 'chat_ids'],
            'facebook': ['page_access_token']
        }

        for platform, fields in required_fields.items():
            if platform not in self.config:
                raise ValueError(f"缺少 {platform} 設定區塊")
            for field in fields:
                if field not in self.config[platform] or not self.config[platform][field]:
                    raise ValueError(f"缺少 {platform}.{field} 或設定為空")

    def _get_random_message(self, category: str) -> str:
        """從內容池中隨機選取一則訊息"""
        if category in self.config['distribution']['content_pool']:
            messages = self.config['distribution']['content_pool'][category]
            return random.choice(messages)
        return f"今天適合做關於 {category} 的活動"

    def _build_message(self) -> str:
        """組合完整的健康提醒訊息"""
        prefix = (
            self.config['line']['message_prefix'] or
            self.config['distribution']['frequency']['message_prefix'] or
            "今日健康提醒："
        )

        categories = random.sample(
            self.config['distribution']['message_types'],
            min(3, len(self.config['distribution']['message_types']))
        )

        lines = [prefix]
        lines.append("")
        for category in categories:
            lines.append(f"• {self._get_random_message(category)}")

        return "\n".join(lines)

    def send_to_line(self, message: str) -> bool:
        """發送訊息到 LINE"""
        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {self.config['line']['token']}",
            "Content-Type": "application/json"
        }
        body = {
            "to": self.config['line']['profile_id'],
            "messages": [{"type": "text", "text": message}]
        }

        try:
            response = requests.post(url, json=body, headers=headers)
            if response.status_code == 200:
                print(f"[{datetime.now()}] ✓ LINE 發送成功: {message[:50]}...")
                return True
            else:
                print(f"[{datetime.now()}] ✗ LINE 發送失敗: {response.text}")
        except Exception as e:
            print(f"[{datetime.now()}] ✗ LINE 發送錯誤: {str(e)}")
        return False

    def send_to_telegram(self, message: str) -> bool:
        """發送訊息到 Telegram"""
        url = "https://api.telegram.org/bot{}/sendMessage".format(
            self.config['telegram']['token']
        )

        results = []
        for chat_id in self.config['telegram']['chat_ids']:
            try:
                params = {
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }
                response = requests.get(url, params=params)
                if response.json().get('ok', False):
                    print(f"[{datetime.now()}] ✓ Telegram (@{chat_id}) 發送成功")
                    results.append(True)
                else:
                    print(f"[{datetime.now()}] ✗ Telegram (@{chat_id}) 發送失敗: {response.text}")
            except Exception as e:
                print(f"[{datetime.now()}] ✗ Telegram (@{chat_id}) 錯誤: {str(e)}")

        return len(results) > 0

    def send_to_facebook(self, message: str) -> bool:
        """發送訊息到 Facebook"""
        # Facebook 需要建立推文或私訊的邏輯
        # 使用 FB Graph API 推播或發布
        # 這是簡化版本，實際需要更多認證和權限

        print(f"[{datetime.now()}] ℹ FB 需要額外設定（推文/私訊 API）")
        print(f"訊息內容: {message}")
        return False

    def distribute(self) -> Dict[str, bool]:
        """統一發送到所有平台"""
        message = self._build_message()
        print(f"\n[{datetime.now()}] === 健康內容發送 ===")
        print(f"訊息: {message}\n")

        results = {
            "LINE": self.send_to_line(message),
            "Telegram": self.send_to_telegram(message),
            "Facebook": self.send_to_facebook(message)
        }

        success_count = sum(results.values())
        print(f"\n[{datetime.now()}] 總計成功: {success_count}/3")

        return results

def main():
    """主程式進入點"""
    try:
        distributor = HealthDistributor()
        distributor.distribute()
    except Exception as e:
        print(f"錯誤: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
