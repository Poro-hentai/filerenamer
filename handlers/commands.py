from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from utils.user_utils import (
    register_user, get_user_pattern, set_user_pattern,
    set_user_metadata, get_user_thumb, delete_user_thumb,
    set_user_thumb, get_user_metadata
)
from utils.thumb_utils import handle_user_thumbnail, get_thumb_path
import os

# Replace this with your admin ID
ADMIN_ID = 5759232282

def add_command_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setpattern", setpattern))
    app.add_handler(CommandHandler("seepattern", seepattern))
    app.add_handler(CommandHandler("delpattern", delpattern))
    app.add_handler(CommandHandler("setmetadata", setmetadata))
    app.add_handler(CommandHandler("setthumb", setthumb))
    app.add_handler(CommandHandler("seethumb", seethumb))
    app.add_handler(CommandHandler("deletethumb", deletethumb))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("help", help_cmd))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    register_user(update.effective_user.id)
    btns = [[
        InlineKeyboardButton("About", callback_data="about"),
        InlineKeyboardButton("Help", callback_data="help")
    ]]
    await update.message.reply_photo(
        photo="https://telegra.ph/file/050a20dace942a60220c0-6afbc023e43fad29c7.jpg",
        caption="👋 Welcome to Advanced File Renamer Bot.\nSend a file and get it renamed with full metadata support!",
        reply_markup=InlineKeyboardMarkup(btns)
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🛠 Available Commands:
/start - Show welcome message
/setpattern <pattern> - Set custom renaming pattern
/seepattern - View current pattern
/delpattern - Reset pattern
/setmetadata <@user|@channel> - Set metadata tag
/setthumb (send photo before this) - Auto-generate thumb via Telegraph
/seethumb - Show saved thumbnail
/deletethumb - Delete your thumbnail
/help - Show help menu
/broadcast <msg> - (Admin) Send message to all users
""")

async def setpattern(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setpattern <pattern>")
        return
    pattern = ' '.join(context.args)
    set_user_pattern(update.effective_user.id, pattern)
    await update.message.reply_text(f"✅ Pattern set:\n`{pattern}`", parse_mode="Markdown")

async def seepattern(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pattern = get_user_pattern(update.effective_user.id)
    await update.message.reply_text(f"📝 Current Pattern:\n`{pattern}`", parse_mode="Markdown")

async def delpattern(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_user_pattern(update.effective_user.id, "{original}_{number}")
    await update.message.reply_text("🔁 Pattern reset to default.")

async def setmetadata(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setmetadata <@channel|@username>")
        return
    set_user_metadata(update.effective_user.id, context.args[0])
    await update.message.reply_text("✅ Metadata updated.")

async def setthumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        await update.message.reply_text("❗ Reply to a photo with /setthumb")
        return
    ok, url = await handle_user_thumbnail(update.message.reply_to_message)
    if ok:
        await update.message.reply_text(f"✅ Thumbnail saved from photo!\n🌐 URL: `{url}`", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to save thumbnail.")

async def seethumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thumb = get_thumb_path(update.effective_user.id)
    if thumb and os.path.exists(thumb):
        await update.message.reply_photo(open(thumb, "rb"))
    else:
        await update.message.reply_text("ℹ️ No thumbnail found.")

async def deletethumb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    delete_user_thumb(update.effective_user.id)
    await update.message.reply_text("🗑️ Thumbnail deleted.")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usage: /broadcast <message>")
        return
    from utils.user_utils import users
    msg = ' '.join(context.args)
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=msg)
        except:
            continue
    await update.message.reply_text("✅ Broadcast sent.")

