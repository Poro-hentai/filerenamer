import os
from telegraph import Telegraph
from utils.user_utils import set_user_thumb, get_user_thumb, delete_user_thumb
from telegram import Message

telegraph = Telegraph()
telegraph.create_account(short_name="RenamerBot")

THUMB_DIR = os.path.join(os.path.dirname(__file__), "..", "thumbnails")

async def handle_user_thumbnail(photo_msg: Message):
    """
    Receives a Telegram photo Message and stores its Telegraph URL + saves thumb locally.
    """
    try:
        file = await photo_msg.bot.get_file(photo_msg.photo[-1].file_id)
        local_path = os.path.join(THUMB_DIR, f"{photo_msg.from_user.id}.jpg")
        await file.download_to_drive(local_path)

        # Upload to Telegraph
        response = telegraph.upload_file(local_path)
        url = "https://telegra.ph" + response[0]["src"]
        set_user_thumb(photo_msg.from_user.id, url)
        return True, url
    except Exception as e:
        print("Thumbnail setup failed:", e)
        return False, None

def get_thumb_path(user_id):
    path = os.path.join(THUMB_DIR, f"{user_id}.jpg")
    return path if os.path.exists(path) else None

def delete_thumb_file(user_id):
    path = get_thumb_path(user_id)
    if path:
        os.remove(path)
    delete_user_thumb(user_id)

