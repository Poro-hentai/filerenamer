
import os, json
from pyrogram import Client, filters
from pyrogram.types import Message

THUMB_FILE = "thumb.json"

def save_thumb(user_id, file_path):
    thumbs = {}
    if os.path.exists(THUMB_FILE):
        with open(THUMB_FILE, "r") as f:
            thumbs = json.load(f)
    thumbs[str(user_id)] = file_path
    with open(THUMB_FILE, "w") as f:
        json.dump(thumbs, f)

def get_thumb(user_id):
    if not os.path.exists(THUMB_FILE): return None
    with open(THUMB_FILE, "r") as f:
        thumbs = json.load(f)
    return thumbs.get(str(user_id))

def del_thumb(user_id):
    if not os.path.exists(THUMB_FILE): return False
    with open(THUMB_FILE, "r") as f:
        thumbs = json.load(f)
    if str(user_id) in thumbs:
        del thumbs[str(user_id)]
        with open(THUMB_FILE, "w") as f:
            json.dump(thumbs, f)
        return True
    return False

@Client.on_message(filters.command("setthumb") & filters.photo)
async def set_thumb_cmd(c, m: Message):
    user_id = m.from_user.id
    file = await m.download(file_name=f"downloads/thumb_{user_id}.jpg")
    save_thumb(user_id, file)
    await m.reply("✅ Thumbnail saved!")

@Client.on_message(filters.command("setthumb") & ~filters.photo)
async def no_photo_thumb(c, m: Message):
    await m.reply("📸 Send a photo with the command /setthumb")

@Client.on_message(filters.command("seethumb"))
async def see_thumb(c, m: Message):
    thumb = get_thumb(m.from_user.id)
    if thumb and os.path.exists(thumb):
        await m.reply_photo(thumb)
    else:
        await m.reply("🚫 No thumbnail set.")

@Client.on_message(filters.command("delthumb"))
async def del_thumb_cmd(c, m: Message):
    if del_thumb(m.from_user.id):
        await m.reply("🗑️ Thumbnail deleted.")
    else:
        await m.reply("🚫 No thumbnail to delete.")

@Client.on_message(filters.photo & ~filters.command(["setthumb"]))
async def auto_thumb_set(c, m: Message):
    user_id = m.from_user.id
    file = await m.download(file_name=f"downloads/thumb_{user_id}.jpg")
    save_thumb(user_id, file)
    await m.reply("✅ Thumbnail auto-set from photo.")
