import sqlite3

conn = sqlite3.connect('passwordmanager.db')

c = conn.cursor()
c.execute(""" CREATE TABLE
                keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title text,
                key text
    ) """)

c.execute(""" CREATE TABLE
                notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title text,
                content text
    ) """)


c.execute(""" CREATE TABLE
                users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name text,
                username text,
                passw text
    ) """)

conn.commit()

conn.close()

