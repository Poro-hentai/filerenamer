from pyrogram import Client, filters
import json
import os
import re

users_file = "users.json"

def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(users_file, "w") as f:
        json.dump(data, f, indent=2)

@Client.on_message(filters.command("autorename"))
async def toggle_autorename(client, message):
    users = load_users()
    user_id = str(message.from_user.id)
    
    if "on" in message.text:
        users[user_id] = users.get(user_id, {})
        users[user_id]["autorename"] = True
        await message.reply("✅ Auto renaming is now **ON**.")
    elif "off" in message.text:
        users[user_id] = users.get(user_id, {})
        users[user_id]["autorename"] = False
        await message.reply("❌ Auto renaming is now **OFF**.")
    else:
        await message.reply("Usage: `/autorename on` or `/autorename off`")
    
    save_users(users)

@Client.on_message(filters.document | filters.video | filters.audio)
async def handle_media(client, message):
    users = load_users()
    user_id = str(message.from_user.id)
    
    file = message.document or message.video or message.audio
    original_name = file.file_name
    
    if user_id not in users or not users[user_id].get("autorename"):
        return  # Auto rename off, ignore

    clean_name = re.sub(r'@\w+', '', original_name)  # remove usernames like @lordshadow
    await message.copy(
        chat_id=message.chat.id,
        caption=f"Renamed: `{clean_name}`"
    )

