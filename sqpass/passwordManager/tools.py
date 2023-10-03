import base64
from prettytable import PrettyTable
import pyperclip
from sqpass.passwordManager.ciphers import decrypt
from sqpass.passwordManager.conf import get_config
import json
import psutil
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from rich.layout import Layout
import sqlite3
from contextlib import contextmanager


def print_note(note, title, sub, markdown=True):
    console = Console()
    note = Markdown(note) if markdown else note

    styles = Panel(
        note,
        box=box.ROUNDED,
        padding=(1, 2),
        title=f"[b red]{title}",
        border_style="bright_blue",
        subtitle=sub,
    )

    console.print(styles)


def print_box(lst, master_pass, clip=False):
    config = get_config()
    colors = config.get("passw_colors")
    table = Table()
    table.add_column("Index", style=colors.get("index"))
    table.add_column("App Name", style=colors.get("appname"))
    table.add_column("Username", style=colors.get("username"))
    table.add_column("Password", style=colors.get("password"))

    for row in lst:
        idx, app_name, username = row[:3]
        res = json.loads(row[3])
        salt = res["salt"]
        iv = res["iv"]
        cipher = res["enc"]
        decipher = decrypt(
            salt, iv, cipher, master_pass.encode()).decode("utf-8")
        table.add_row(str(idx), app_name, username, decipher)
    if clip:
        pyperclip.copy(decipher)
        return None
    else:
        console = Console()
        console.print(table)
        return ""


def print_keys(row, master_pass, clip=False):
    table = Table()
    fields = ['Index', 'Title', "Key"]
    for field in fields:
        table.add_column(field)

    for data in row:
        data_cipher = json.loads(data[2])
        salt, iv, ct = data_cipher.values()
        decipher = decrypt(
            salt, iv, ct, master_pass.encode()).decode()

        table.add_row(str(data[0]), data[1], decipher)
    if clip:
        pyperclip.copy(decipher)
        return ""
    else:
        console = Console()
        console.print(table)
        return ""


def print_note_list(row):
    notes = Table()
    fields = ["Index", "Title", "Content"]
    for field in fields:
        notes.add_column(field)
    for idx, title, cont, _ in row:
        notes.add_row(
            str(idx), title.strip()[:20], base64.b64decode(
                cont).decode()[:20] + "..."
        )
    console = Console()
    console.print(notes)
    return ""


def is_process_running(command):
    for proc in psutil.process_iter(attrs=["cmdline"]):
        try:
            cmdline = proc.info.get("cmdline")
            if cmdline is not None and command in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
    return False


@contextmanager
def opendb(path):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    try:
        yield cur
    except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
        raise
    finally:
        conn.commit()
        conn.close()


@contextmanager
def dbfetch(path, query, data=None):
    try:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        if data is None:
            cur.execute(query)
        else:
            cur.execute(query, data)
        yield cur.fetchall()
    except sqlite3.DatabaseError as e:
        print("Database not found, Try to run `sq-init`")
        exit()
    finally:
        cur.close()
