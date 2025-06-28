import os
import re
import uuid
import subprocess
from utils.user_utils import get_user_metadata

# Return thumbnail path based on user ID
def get_thumb_path(user_id):
    return f"downloads/thumb_{user_id}.jpg"  # you can adjust this path if needed

# Generate a clean and formatted filename using a pattern
def generate_filename(original, user_id, pattern="{original}_{number}", counter=1):
    base, ext = os.path.splitext(original)
    base = re.sub(r'[<>:"/\\|?*]', '', base)  # Remove invalid characters for file names
    filename = pattern.replace("{original}", base).replace("{number}", str(counter))
    return filename + ext

# Check if file is a video
def is_video(filename):
    return filename.lower().endswith((".mp4", ".mkv", ".mov", ".avi"))

# Check if file is a PDF
def is_pdf(filename):
    return filename.lower().endswith(".pdf")

# Allow all files (you can add your own filters if needed)
def is_supported(filename):
    return True

# Use ffmpeg to remux audio/subtitle metadata and add user tag
def remux_with_metadata(input_path, output_path, user_id):
    user_tag = get_user_metadata(user_id)
    if not user_tag:
        return False

    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "s,a",
             "-show_entries", "stream=index,codec_type:stream_tags=language,title",
             "-of", "json", input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        info = eval(result.stdout) if result.stdout else {}
        streams = info.get("streams", [])
    except Exception as e:
        print("ffprobe failed:", e)
        return False

    ffmpeg_args = ["ffmpeg", "-i", input_path, "-map", "0", "-c", "copy"]
    for stream in streams:
        index = stream.get("index")
        stype = stream.get("codec_type")
        if stype in ["audio", "subtitle"]:
            meta_key = f"-metadata:s:{'a' if stype == 'audio' else 's'}:{index}"
            existing_title = stream.get("tags", {}).get("title", "")
            new_title = f"{existing_title} - {user_tag}".strip()
            ffmpeg_args.extend([meta_key, new_title])

    ffmpeg_args.append(output_path)

    try:
        subprocess.run(ffmpeg_args, check=True)
        return True
    except Exception as e:
        print("ffmpeg metadata remux failed:", e)
        return False

# Remove temporary files
def cleanup_temp_files(*paths):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")
