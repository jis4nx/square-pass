from prettytable import PrettyTable
from passwordManager.ciphers import encrypt, decrypt



def print_box(lst, master_pass):

    headers = ["App Name", "Username", "Password"]
    t = PrettyTable(headers)
    
    for row in lst:
        encPass = str(row[2]).encode()
        username , app_name = row[0] , row[1]
        decipher = decrypt(encPass, master_pass.encode()).decode()
        conts = [username, app_name, decipher]
        t.add_row(conts)
    return t 


