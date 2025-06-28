import os
from telegraph import Telegraph
from telegram import Message
from utils.user_utils import set_user_thumb, get_user_thumb, delete_user_thumb

# Initialize Telegraph client
telegraph = Telegraph()
telegraph.create_account(short_name="RenamerBot")

# Thumbnail directory
THUMB_DIR = os.path.join(os.path.dirname(__file__), "..", "thumbnails")

async def handle_user_thumbnail(photo_msg: Message):
    """
    Receives a Telegram photo Message, saves locally and uploads to Telegraph.
    Stores Telegraph URL and local thumbnail path for later use.
    """
    try:
        user_id = photo_msg.from_user.id
        file = await photo_msg.bot.get_file(photo_msg.photo[-1].file_id)
        local_path = os.path.join(THUMB_DIR, f"{user_id}.jpg")
        await file.download_to_drive(local_path)

        # Upload to Telegraph
        response = telegraph.upload_file(local_path)
        url = "https://telegra.ph" + response[0]["src"]

        # Save URL in JSON data
        set_user_thumb(user_id, url)
        return True, url

    except Exception as e:
        print(f"[Thumbnail Setup Error] {e}")
        return False, None

def get_thumb_path(user_id):
    """
    Returns local path to user's thumbnail if it exists, else None.
    """
    path = os.path.join(THUMB_DIR, f"{user_id}.jpg")
    return path if os.path.exists(path) else None

def delete_thumb_file(user_id):
    """
    Deletes both the local thumbnail file and its JSON reference.
    """
    path = get_thumb_path(user_id)
    if path:
        try:
            os.remove(path)
        except Exception as e:
            print(f"[Thumbnail Delete Error] {e}")
    delete_user_thumb(user_id)
