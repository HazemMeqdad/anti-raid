import sqlite3

db = sqlite3.connect("db.sqlite")
cr = db.cursor()

cr.execute(
    """CREATE TABLE IF NOT EXISTS anti(
    id INTEGER PRIMARY KEY, 
    role_create INTEGER DEFAULT 0, 
    role_delete INTEGER DEFAULT 0, 
    channel_create INTEGER DEFAULT 0, 
    channel_delete INTEGER DEFAULT 0, 
    ban INTEGER DEFAULT 0, 
    kick INTEGER DEFAULT 0
    )"""
)


def commit():
    db.commit()


def insert(user_id):
    cr.execute("INSERT OR IGNORE INTO anti(id) VALUES(?)", (user_id,))
    commit()


def insert_action(user_id, action, new_limit: int):
    if action not in ['role_create', 'role_delete', "channel_create", "channel_delete", "ban", "kick"]:
        raise TypeError("Bad action name")
    insert(user_id)
    cr.execute(f"UPDATE anti set '{action}' = ? WHERE id = ?", (new_limit, user_id))
    commit()


def select_action(user_id, action):
    if action not in ['role_create', 'role_delete', "channel_create", "channel_delete", "ban", "kick"]:
        raise TypeError("Bad action name")
    insert(user_id)
    date = cr.execute(f"SELECT {action} FROM anti WHERE id = ?", (user_id,))
    return date.fetchone()[0]


def reset():
    cr.execute("DELETE FROM anti")
    commit()
