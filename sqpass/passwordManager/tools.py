from sqpass.passwordManager.ciphers import encrypt, decrypt
from sqpass.passwordManager.conf import get_config
import json
import psutil
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from rich.layout import Layout


def print_note(note, title, sub, markdown=True):

    console = Console()
    layout = Layout()

    note = Markdown(note) if markdown else note

    styles = Panel(
        note,
        box=box.ROUNDED,
        padding=(1, 2),
        title=f"[b red]{title}",
        border_style="bright_blue",
        subtitle=sub
    )

    console.print(styles)


def print_box(lst, master_pass):
    config = get_config()
    colors = config.get('passw_colors')
    table = Table()
    table.add_column("Index", style=colors.get('index'))
    table.add_column("Username", style=colors.get('username'))
    table.add_column("App Name", style=colors.get('appname'))
    table.add_column("Password", style=colors.get('password'))

    for row in lst:
        idx, username, app_name = row[:3]
        res = json.loads(row[3])
        salt = res['salt']
        iv = res['iv']
        cipher = res['enc']
        decipher = decrypt(
            salt, iv, cipher, master_pass.encode()).decode('utf-8')
        table.add_row(str(idx), username, app_name, decipher)
    console = Console()
    console.print(table)
    return ""


def is_process_running(command):
    for proc in psutil.process_iter(attrs=['cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline == command:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
