from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from .commands import help_cmd, start

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_caption(
            caption="📢 *About Bot*\nThis bot renames files up to 4GB, edits metadata (video, audio, subtitle), and returns ultra-fast renamed files using a private channel.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="back")]
            ])
        )

    elif query.data == "help":
        await query.message.delete()
        await help_cmd(update, context)

    elif query.data == "back":
        await query.message.delete()
        await start(update, context)

    elif query.data == "close":
        await query.message.delete()

