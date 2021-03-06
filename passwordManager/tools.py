from prettytable import PrettyTable
from passwordManager.ciphers import encrypt, decrypt



from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from rich.align import Align
from rich.console import Console
from rich.layout import Layout




def print_note(note,title,sub,markdown=True):

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

    headers = ["Index","App Name", "Username", "Password"]
    t = PrettyTable(headers)
    
    for row in lst:
        idx = row[0]
        encPass = str(row[3]).encode()
        username , app_name = row[1] , row[2]
        decipher = decrypt(encPass, master_pass.encode()).decode()
        conts = [idx, username, app_name, decipher]
        t.add_row(conts)
    return t 


