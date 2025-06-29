from pyrogram import Client, filters
import json
import os

caption_file = "captions.json"

def load_captions():
    if os.path.exists(caption_file):
        with open(caption_file, "r") as f:
            return json.load(f)
    return {}

def save_captions(data):
    with open(caption_file, "w") as f:
        json.dump(data, f, indent=2)

@Client.on_message(filters.command("setcaption"))
async def set_caption(client, message):
    user_id = str(message.from_user.id)
    if len(message.command) < 2:
        await message.reply("Usage: `/setcaption your caption here`", quote=True)
        return

    caption = message.text.split(None, 1)[1]
    captions = load_captions()
    captions[user_id] = caption
    save_captions(captions)
    await message.reply("✅ Caption saved!")

@Client.on_message(filters.document | filters.video | filters.audio)
async def apply_caption(client, message):
    user_id = str(message.from_user.id)
    captions = load_captions()
    if user_id not in captions:
        return

    await message.copy(
        chat_id=message.chat.id,
        caption=captions[user_id]
    )
