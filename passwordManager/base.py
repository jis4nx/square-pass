import sqlite3,base64, getpass
from passwordManager.ciphers import encrypt, decrypt
from prettytable import PrettyTable

def print_box(lst, master_pass):
    t = PrettyTable(["App Name", "Username", "Password"])
    for row in lst:
        encPass = str(row[2]).encode()
        username = row[1]
        app_name = row[0]
        decipher = decrypt(encPass, master_pass.encode()).decode()
        t.add_row([username, app_name, decipher])
    return t 

def dbconnect():
    try:
        conn = sqlite3.connect("passwordmanager.db")
        return conn
    except Exception as error:
        print("Failed to Connect Database", error)

def insert(MASTERPASS):
    try:
        master_pass= MASTERPASS
        connection = dbconnect()
        cur = connection.cursor()
        
        m_pass = getpass.getpass("MasterKey: ")

        if m_pass == master_pass:

            app_name = str(input("app_name :"))
            u_name = str(input("Username: "))
            enc = encrypt(getpass.getpass("Password: ").encode(), m_pass.encode())
            with connection:
                InsertQuery = f"INSERT INTO users (app_name,username, passw) VALUES (:appname ,:u_name,:pass)"
                cur.execute(InsertQuery,{
                    "appname": app_name,
                    "u_name":u_name,
                    "pass":enc.decode()
                })
            
                print(f"[+]Successfully Added for {u_name}")
                input()
    except Exception as error:
        print("Failed to Insert Into Database", error)

def viewdb_by_appname(MASTERPASS,APP_NAME):
    master_pass = MASTERPASS
    m_pass = getpass.getpass("MasterKey : ")
    if m_pass == master_pass :
        try:
            connection = dbconnect()
            cur = connection.cursor()
            app_name = APP_NAME
            readquery = "SELECT * FROM users WHERE app_name=:app_name;"
            with connection:
                cur.execute(readquery,{"app_name":app_name})
                rows = cur.fetchall() 
            content_table = print_box(rows, m_pass)
            print(content_table)
        except Exception as error:
            print("Failed to Read Database", error)


def viewdb_by_username(MASTERPASS,USER_NAME):
    master_pass = MASTERPASS
    m_pass = getpass.getpass("MasterKey: ")
    if m_pass == master_pass:
        try:
            connection = dbconnect()
            cur = connection.cursor()
            username = USER_NAME
            readquery = "SELECT * FROM users WHERE username=:username;"
            with connection:
                cur.execute(readquery,{"username":username})
                rows = cur.fetchall() 
            content_table = print_box(rows, m_pass)
            print(content_table)
        except Exception as error:
            print("Failed to Read Database", error)


def viewall(MASTERPASS):
    master_pass = MASTERPASS
    # m_pass = getpass.getpass("MasterKey: ")
    m_pass = "shoaibislam"
    if m_pass == master_pass :
        try:
            connection = dbconnect()
            cur = connection.cursor()
            readquery = "SELECT * FROM users;"

            with connection:

                cur.execute(readquery)
                rows = cur.fetchall() 
            content_table = print_box(row, m_pass)
            print(content_table)
        except Exception as error:
            print("Failed to Read Database", error)
