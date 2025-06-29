from pyrogram import Client, filters
import json
import os

series_file = "series.json"

def load_series():
    if os.path.exists(series_file):
        with open(series_file, "r") as f:
            return json.load(f)
    return {}

def save_series(data):
    with open(series_file, "w") as f:
        json.dump(data, f, indent=2)

@Client.on_message(filters.command("seriesrenaming"))
async def series_control(client, message):
    series_data = load_series()
    user_id = str(message.from_user.id)

    if "off" in message.text:
        if user_id in series_data:
            del series_data[user_id]
            save_series(series_data)
        await message.reply("🛑 Series renaming disabled.")
        return

    if "on" in message.text:
        parts = message.text.split(None, 3)
        if len(parts) < 4:
            await message.reply("Usage: `/seriesrenaming on Naruto {episode} @lordshadow 5`")
            return

        base = parts[1]
        ep_placeholder = parts[2]
        start = int(parts[3])
        series_data[user_id] = {"template": base, "ep": start, "placeholder": ep_placeholder}
        save_series(series_data)
        await message.reply(f"📺 Series renaming enabled starting from episode {start}")

@Client.on_message(filters.document | filters.video | filters.audio)
async def series_renamer(client, message):
    user_id = str(message.from_user.id)
    series_data = load_series()

    if user_id not in series_data:
        return

    info = series_data[user_id]
    current_ep = info["ep"]
    new_name = info["template"].replace(info["placeholder"], f"E{current_ep:02}")
    
    await message.copy(
        chat_id=message.chat.id,
        caption=f"Series Renamed: `{new_name}`"
    )
    series_data[user_id]["ep"] += 1
    save_series(series_data)

