
from pyrogram import Client, filters
from config import Config
import json

@Client.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(Config.START_TEXT)

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(Config.HELP_TEXT)

@Client.on_message(filters.command("about"))
async def about_command(client, message):
    await message.reply_text(Config.ABOUT_TEXT)
