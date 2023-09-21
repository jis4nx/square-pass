import sqlite3
import os
import platform
db_paths = {
    'Linux': os.path.expanduser("~/.local/share/pass.db"),
    'Windows': os.path.expanduser("~/AppData/pass.db")
}
db_path = db_paths.get(platform.system())


def check_db_file():
    if os.path.exists(db_path):
        return True
    return False


def create_database():

    conn = sqlite3.connect(db_path)

    c = conn.cursor()
    print('Creating database.....')
    c.execute(""" CREATE TABLE
                    keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title text,
                    key text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """)

    c.execute(""" CREATE TABLE
                    notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title text,
                    content text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """)

    c.execute(""" CREATE TABLE
                    passw (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    app_name text,
                    username text,
                    passwd text,
                    date DATETIME DEFAULT CURRENT_TIMESTAMP
        ) """)

    conn.commit()

    print(f"Create database successfully at {db_path}")
    conn.close()


if __name__ == "__main__":
    create_database()
