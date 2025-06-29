
import os

class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID"))

    START_TEXT = "👋 Welcome to the Renaming Bot!\nUse /help to know commands."
    HELP_TEXT = """📚 **Bot Commands:**
/setmetadata - Set subtitle/audio metadata
/seemetadata - View current metadata
/delmetadata - Remove all metadata
/seriesrenaming on/off - Enable/Disable series auto rename
/autorename on/off - Enable/Disable auto rename
/setcaption - Set caption
/broadcast - Send message to all users
/stats - Bot usage stats
/about - About this bot"""
    ABOUT_TEXT = "🤖 **Bot Name**: RenamerBot\n🚀 Fast file renamer using private channel\n🧑‍💻 Developer: @YourUsername"
