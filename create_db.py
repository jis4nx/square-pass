import sqlite3

conn = sqlite3.connect('passwordmanager.db')

c = conn.cursor()
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

conn.close()

