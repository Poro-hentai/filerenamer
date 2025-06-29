from pyrogram import Client, filters
import json
import os

metadata_file = "metadata.json"

def load_metadata():
    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as f:
            return json.load(f)
    return {}

def save_metadata(data):
    with open(metadata_file, "w") as f:
        json.dump(data, f, indent=2)

@Client.on_message(filters.command("setmetadata"))
async def set_metadata(client, message):
    user_id = str(message.from_user.id)
    data = load_metadata()
    
    if len(message.command) < 2:
        await message.reply("Usage: `/setmetadata subtitle:English,audio:Japanese`", quote=True)
        return
    
    parts = message.text.split(None, 1)[1]
    items = dict(item.split(":") for item in parts.split(","))
    
    data[user_id] = items
    save_metadata(data)
    
    await message.reply(f"✅ Metadata set for you:\n{items}", quote=True)

@Client.on_message(filters.command("seemetadata"))
async def see_metadata(client, message):
    user_id = str(message.from_user.id)
    data = load_metadata()
    if user_id in data:
        await message.reply(f"Your metadata:\n{data[user_id]}", quote=True)
    else:
        await message.reply("❌ You haven't set any metadata.", quote=True)

@Client.on_message(filters.command("delmetadata"))
async def delete_metadata(client, message):
    user_id = str(message.from_user.id)
    data = load_metadata()
    if user_id in data:
        del data[user_id]
        save_metadata(data)
        await message.reply("🗑 Metadata removed.")
    else:
        await message.reply("❌ No metadata found for you.")
