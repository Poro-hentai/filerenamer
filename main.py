import asyncio
from pyrogram import Client, idle
from config import Config
import os

bot = Client(
    "renamer-bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins={"root": "bot/handlers"}
)

async def main():
    print("⏳ Starting bot...")
    await bot.start()
    print("🤖 Bot is running...")
    await idle()
    await bot.stop()

if __name__ == "__main__":
    asyncio.run(main())
