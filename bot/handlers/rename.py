import os
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.plugins.thumb import get_thumb
import time

DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

@Client.on_message(filters.document | filters.video | filters.audio)
async def rename_file(client: Client, message: Message):
    user_id = message.from_user.id
    media = message.document or message.video or message.audio

    original_file_name = media.file_name
    original_file_size = media.file_size

    status = await message.reply_text("⏳ Starting download...")

    start_time = time.time()
    downloaded_path = await message.download(file_name=f"{DOWNLOADS}/{original_file_name}")
    end_time = time.time()

    await status.edit_text(f"✅ Downloaded in {int(end_time - start_time)} seconds.\n\n🔁 Renaming file...")

    # Simple renaming logic (you can replace with your own logic or command-based name)
    new_name = original_file_name.replace(" ", "_")
    renamed_path = os.path.join(DOWNLOADS, new_name)
    os.rename(downloaded_path, renamed_path)

    thumb_path = get_thumb(user_id)

    async def progress(current, total):
        percent = int(current * 100 / total)
        bar = "▓" * (percent // 10) + "░" * (10 - percent // 10)
        try:
            await status.edit_text(f"📤 Uploading...\n[{bar}] {percent}%")
        except:
            pass

    await message.reply_document(
        document=renamed_path,
        caption=f"✅ Renamed to: `{new_name}`",
        thumb=thumb_path if thumb_path else None,
        progress=progress
    )

    await status.delete()

    # Optional cleanup
    try:
        os.remove(renamed_path)
    except Exception as e:
        print(f"Cleanup failed: {e}")
