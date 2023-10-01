import os
import getpass
import platform
import sqlite3
from sqpass.passwordManager.ciphers import finalhash
from sqpass.create_db import create_database, db_path
from sqpass.passwordManager.conf import get_config_path, setup_config

password_dirs = {
    "Linux": os.path.expanduser("~/.local/share/sqpass/"),
    "Windows": os.path.expanduser("~\\AppData\\sqpass\\"),
}

password_path = os.path.join(password_dirs.get(platform.system()), "pass.key")


def createpass(dir, txt):
    try:
        os.makedirs(dir)
        with open(password_path, "wb") as f:
            f.write(txt)
        print(f"Passkey created at {password_path}")
    except Exception as e:
        print(f"Failed to create passkey: {e}")


def check_db_table():
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            rows = cur.execute("""SELECT * FROM passw""").fetchall()
            if rows:
                userInp = input(
                    f"Database already exist at {db_path}\n Do you wanna override? [Y/N]: "
                )
                if userInp.lower() == "y":
                    os.remove(db_path)
                    create_database()
        except sqlite3.OperationalError as e:
            create_database()
    else:
        create_database()


def is_passw_file():
    path = password_dirs.get(platform.system(), "")
    if os.path.exists(path):
        return True
    return False


def setup():
    salt = "xx01"
    while True:
        userInp = getpass.getpass("Create your Masterpass: ")
        userInp1 = getpass.getpass("Confirm Masterpass: ")
        if userInp == userInp1:
            keysalt = (userInp[-4:] + salt) * 2
            try:
                hashed_mpass = finalhash(userInp.encode(), keysalt.encode())
                os_name = platform.system()
                if os_name in password_dirs:
                    createpass(password_dirs[os_name], hashed_mpass.encode())
                else:
                    print("Unsupported OS")
            except ValueError:
                print("Choose a password between 4-32 characters long!")
            break


def setmain():
    if not is_passw_file():
        setup()
    else:
        print(f"Passkey Found! {password_path}")
    check_db_table()
    if not os.path.exists(os.path.join(get_config_path(), "config.yaml")):
        setup_config()
    else:
        path = os.path.join(get_config_path(), "config.yaml")
        print(f"Config file Found! {path}")
