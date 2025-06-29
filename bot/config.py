import os

class Config:
    API_ID = int(os.getenv("API_ID", "23454999"))
    API_HASH = os.getenv("API_HASH", "58ba01dde6198b22a48b2f839b5346eb")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7363840731:AAHmxAoxl_VPrq3mbFT-Okjq4T5O6jRtHWE")
    ADMIN_ID = int(os.getenv("ADMIN_ID", "5759232282"))
    PRIVATE_CHANNEL_ID = int(os.getenv("PRIVATE_CHANNEL_ID", "-1002453946876"))


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
