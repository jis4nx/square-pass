import sqlite3
import os
import platform

db_paths = {
    "Linux": os.path.expanduser("~/.local/share/sqpass/"),
    "Windows": os.path.expanduser("~\\AppData\\sqpass\\"),
}
db_dir = db_paths.get(platform.system())
db_path = os.path.join(db_dir, "pass.db")


def check_db_file():
    if os.path.exists(db_path):
        return True
    return False


def clear_db():
    if check_db_file:
        os.remove(db_path)
        print("Rebuilding database...")
        create_database()
        print("[+]Done")


def create_database():
    if not check_db_file:
        os.makedirs(db_dir)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    print("Creating database.....")
    c.execute(
        """ CREATE TABLE
                    keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title text,
                    key text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """
    )

    c.execute(
        """ CREATE TABLE
                    notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title text,
                    content text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """
    )

    c.execute(
        """ CREATE TABLE
                    passw (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name text,
                    username text,
                    passwd text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
