import os
import datetime
from telegram import Update, InputFile
from telegram.ext import ContextTypes, CommandHandler
from utils.user_utils import get_all_users
from utils.file_utils import cleanup_temp_files

# Path config
JSON_DIR = "data"
BACKUP_STATE_FILE = "data/backup_state.json"
CHANNEL_ID = -1002641723741  # your channel

def add_json_handlers(app):
    app.add_handler(CommandHandler("downloadjson", download_json))

async def download_json(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 5759232282:
        await update.message.reply_text("❌ You are not authorized.")
        return

    await update.message.reply_text("📦 Sending all JSON files...")
    for file_name in os.listdir(JSON_DIR):
        if file_name.endswith(".json"):
            path = os.path.join(JSON_DIR, file_name)
            await update.message.reply_document(document=InputFile(path), caption=file_name)

# === Daily Backup Function ===

async def daily_json_backup(context: ContextTypes.DEFAULT_TYPE):
    from json import load, dump

    # Load backup state
    if os.path.exists(BACKUP_STATE_FILE):
        with open(BACKUP_STATE_FILE) as f:
            state = load(f)
    else:
        state = {"count": 0, "last_msg_id": None}

    state["count"] += 1

    # Send header message
    header = await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=f"🗂 Sending JSON Backup #{state['count']}"
    )

    # Pin new message & unpin old
    if state["last_msg_id"]:
        try:
            await context.bot.unpin_chat_message(CHANNEL_ID, state["last_msg_id"])
        except: pass

    await context.bot.pin_chat_message(CHANNEL_ID, header.message_id)
    state["last_msg_id"] = header.message_id

    # Send all JSONs
    for file_name in os.listdir(JSON_DIR):
        if file_name.endswith(".json"):
            path = os.path.join(JSON_DIR, file_name)
            await context.bot.send_document(chat_id=CHANNEL_ID, document=InputFile(path), caption=file_name)

    # Save updated state
    with open(BACKUP_STATE_FILE, "w") as f:
        dump(state, f, indent=2)
