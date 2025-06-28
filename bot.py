# === advanced_renamer_bot/bot.py ===

import os
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder
from handlers.commands import add_command_handlers
from handlers.files import file_handler
from handlers.buttons import button_handler
from telegram.ext import MessageHandler, CallbackQueryHandler, filters
from utils.user_utils import ensure_directories

# === Flask Keep Alive ===
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Bot is running!"
def run_flask(): flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# === Init ===
TOKEN = "7363840731:AAGoUphGGS-bkfLvidi41pAY-rdZ1CbBFvo"
ensure_directories()

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()

    # Command + button handlers
    add_command_handlers(app)
    app.add_handler(CallbackQueryHandler(button_handler))

    # File handler
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, file_handler))
    app.run_polling(drop_pending_updates=True)

