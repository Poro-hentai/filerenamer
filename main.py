import asyncio
from pyrogram import Client
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

if __name__ == "__main__":
    from pyrogram.idle import idle
    asyncio.run(main())
