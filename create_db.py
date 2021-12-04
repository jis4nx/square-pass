
import sqlite3

conn = sqlite3.connect('passwordmanager.db')

c = conn.cursor()

c.execute(""" CREATE TABLE pass(
                mspass text,
                xx text),
                users (
                app_name text,
                username text,
                passw text
) """)

conn.commit()

conn.close()

