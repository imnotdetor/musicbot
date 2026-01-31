from utils.database import get_queue, set_queue, clear_queue

# RAM cache (fast)
QUEUE = {}


def load_queue(chat_id: int):
    QUEUE[chat_id] = get_queue(chat_id)


def add_song(chat_id: int, song: dict):
    if chat_id not in QUEUE:
        load_queue(chat_id)

    QUEUE[chat_id].append(song)
    set_queue(chat_id, QUEUE[chat_id])


def get_next_song(chat_id: int):
    if chat_id not in QUEUE or not QUEUE[chat_id]:
        return None

    song = QUEUE[chat_id].pop(0)
    set_queue(chat_id, QUEUE[chat_id])
    return song


def view_queue(chat_id: int):
    if chat_id not in QUEUE:
        load_queue(chat_id)
    return QUEUE[chat_id]


def reset_queue(chat_id: int):
    QUEUE.pop(chat_id, None)
    clear_queue(chat_id)