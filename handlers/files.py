import os
import uuid
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from utils.user_utils import (
    register_user, get_user_pattern, get_user_metadata,
    get_thumb_path
)
from utils.file_utils import (
    generate_filename, is_video, is_pdf,
    remux_with_metadata, cleanup_temp_files
)
from utils.episode_quality import extract_episode_quality

# Channel to upload and re-fetch from
CHANNEL_ID = -1002641723741

file_counter = {}

async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    register_user(user_id)

    tg_file = update.message.document or update.message.video
    if not tg_file:
        await update.message.reply_text("❗ Send a document or video file.")
        return

    # File size check (4GB max)
    if tg_file.file_size > 4 * 1024 * 1024 * 1024:
        await update.message.reply_text("❌ File too large. Max limit is 4GB.")
        return

    # Setup
    msg = await update.message.reply_text("📥 Downloading file...")
    orig_name = tg_file.file_name or "file"
    caption = update.message.caption or orig_name

    # Generate filename from pattern
    counter = file_counter.get(user_id, 1)
    user_pattern = get_user_pattern(user_id)
    ep, ql = extract_episode_quality(caption)
    base_name = orig_name.rsplit('.', 1)[0]
    new_name = user_pattern.replace("{original}", base_name).replace("{number}", str(counter)).replace("{episode}", ep).replace("{quality}", ql)
    new_name += os.path.splitext(orig_name)[1]
    file_counter[user_id] = counter + 1

    # Download path
    dl_path = f"downloads/{uuid.uuid4().hex}_{new_name}"
    await tg_file.get_file().download_to_drive(dl_path)

    await msg.edit_text("🧠 Processing metadata...")

    # Remux metadata if video
    final_path = dl_path
    if is_video(new_name):
        output_path = f"downloads/{uuid.uuid4().hex}_edited_{new_name}"
        if remux_with_metadata(dl_path, output_path, user_id):
            final_path = output_path

    # Thumbnail logic
    thumb_path = get_thumb_path(user_id)
    thumb = open(thumb_path, "rb") if thumb_path else None

    # Upload to private channel
    try:
        await msg.edit_text("📤 Uploading to private channel...")
        if is_video(new_name):
            sent_msg = await context.bot.send_video(
                chat_id=CHANNEL_ID,
                video=open(final_path, "rb"),
                caption=new_name,
                thumbnail=thumb,
                supports_streaming=True
            )
            file_id = sent_msg.video.file_id
            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=file_id,
                caption=new_name,
                supports_streaming=True
            )
        else:
            sent_msg = await context.bot.send_document(
                chat_id=CHANNEL_ID,
                document=open(final_path, "rb"),
                caption=new_name,
                thumbnail=thumb
            )
            file_id = sent_msg.document.file_id
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file_id,
                caption=new_name
            )
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Upload failed:\n`{e}`", parse_mode="Markdown")

    # Cleanup
    await asyncio.sleep(5)
    cleanup_temp_files(dl_path, final_path)
    if thumb: thumb.close()

