import asyncio
import os
from telegram import Bot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def Bot_sendMessage(message, chat_id=None):
    token = TOKEN
    target = chat_id or CHAT_ID
    if not token or not target:
        print("[TG] TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 未設定，略過通知")
        return

    async def send_message(message):
        bot = Bot(token=token)
        max_len = 4096
        text = str(message)
        for i in range(0, len(text), max_len):
            await bot.send_message(chat_id=target, text=text[i:i + max_len])

    asyncio.run(send_message(message))
