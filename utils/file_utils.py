import os
import re
import uuid
import subprocess
from utils.user_utils import get_user_metadata


def get_thumb_path(user_id):
    return f"thumbnails/{user_id}.jpg"


def generate_filename(original, user_id, pattern="{original}_{number}", counter=1):
    base, ext = os.path.splitext(original)
    base = re.sub(r'[<>:"/\\|?*]', '', base)  # Remove invalid characters
    filename = pattern.replace("{original}", base).replace("{number}", str(counter))
    return filename + ext


def is_video(filename):
    return filename.lower().endswith((".mp4", ".mkv", ".mov", ".avi"))


def is_pdf(filename):
    return filename.lower().endswith(".pdf")


def is_supported(filename):
    return True  # Allow all file types


def remux_with_metadata(input_path, output_path, user_id):
    user_tag = get_user_metadata(user_id)
    if not user_tag:
        return False

    # Get subtitle/audio stream info using ffprobe
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

    # Build ffmpeg args to modify metadata
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


def cleanup_temp_files(*paths):
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Error cleaning up {path}: {e}")
