
import os
import json
from datetime import datetime

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
THUMB_DIR = os.path.join(BASE_DIR, "..", "thumbnails")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "..", "downloads")

USERS_FILE = os.path.join(DATA_DIR, "users.json")
THUMBS_FILE = os.path.join(DATA_DIR, "thumbs.json")
METADATA_FILE = os.path.join(DATA_DIR, "metadata.json")
PATTERNS_FILE = os.path.join(DATA_DIR, "patterns.json")

# === Global Cache ===
users = {}
thumbs = {}
metadata = {}
patterns = {}

def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(THUMB_DIR, exist_ok=True)
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    load_all_json()

# === JSON Helpers ===
def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_all_json():
    global users, thumbs, metadata, patterns
    users = load_json(USERS_FILE)
    thumbs = load_json(THUMBS_FILE)
    metadata = load_json(METADATA_FILE)
    patterns = load_json(PATTERNS_FILE)

def save_all_json():
    save_json(USERS_FILE, users)
    save_json(THUMBS_FILE, thumbs)
    save_json(METADATA_FILE, metadata)
    save_json(PATTERNS_FILE, patterns)

# === User Functions ===
def register_user(user_id):
    uid = str(user_id)
    if uid not in users:
        users[uid] = str(datetime.now())
        save_json(USERS_FILE, users)

def get_user_pattern(user_id):
    return patterns.get(str(user_id), "{original}_{number}")

def set_user_pattern(user_id, pat):
    patterns[str(user_id)] = pat
    save_json(PATTERNS_FILE, patterns)

def get_user_metadata(user_id):
    return metadata.get(str(user_id), "")

def set_user_metadata(user_id, value):
    metadata[str(user_id)] = value
    save_json(METADATA_FILE, metadata)

def get_user_thumb(user_id):
    return thumbs.get(str(user_id))

def set_user_thumb(user_id, url):
    thumbs[str(user_id)] = url
    save_json(THUMBS_FILE, thumbs)

def delete_user_thumb(user_id):
    thumbs.pop(str(user_id), None)
    save_json(THUMBS_FILE, thumbs)
