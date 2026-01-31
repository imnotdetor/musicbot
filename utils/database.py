from pymongo import MongoClient
import os

# ---------------- CONFIG ---------------- #

MONGO_URI = os.getenv("MONGO_URI")
TEST_MODE = False

# ---------------- CONNECTION ---------------- #

if not MONGO_URI:
    # 👉 Pydroid / local testing fallback
    TEST_MODE = True
    print("[DB] MONGO_URI not set → TEST MODE (in-memory DB)")
else:
    client = MongoClient(MONGO_URI)
    db = client["AdvanceMusicBot"]
    queues = db["queues"]
    playlists = db["playlists"]
    users = db["users"]

# ---------------- IN-MEMORY DB (TEST MODE) ---------------- #

_MEMORY_QUEUES = {}
_MEMORY_PLAYLISTS = {}

# ---------------- QUEUE HELPERS ---------------- #

def get_queue(chat_id: int):
    if TEST_MODE:
        return _MEMORY_QUEUES.get(chat_id, [])

    data = queues.find_one({"chat_id": chat_id})
    if not data:
        return []
    return data.get("songs", [])


def set_queue(chat_id: int, songs: list):
    if TEST_MODE:
        _MEMORY_QUEUES[chat_id] = songs
        return

    queues.update_one(
        {"chat_id": chat_id},
        {"$set": {"songs": songs}},
        upsert=True
    )


def clear_queue(chat_id: int):
    if TEST_MODE:
        _MEMORY_QUEUES.pop(chat_id, None)
        return

    queues.delete_one({"chat_id": chat_id})


# ---------------- PLAYLIST HELPERS ---------------- #

def add_playlist_song(user_id: int, song: dict):
    if TEST_MODE:
        _MEMORY_PLAYLISTS.setdefault(user_id, []).append(song)
        return

    playlists.update_one(
        {"user_id": user_id},
        {"$push": {"songs": song}},
        upsert=True
    )


def get_playlist(user_id: int):
    if TEST_MODE:
        return _MEMORY_PLAYLISTS.get(user_id, [])

    data = playlists.find_one({"user_id": user_id})
    if not data:
        return []
    return data.get("songs", [])