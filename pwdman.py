from Crypto.Cipher import AES
import base64
import os, psycopg2, subprocess, getpass, random, secrets


db_name = "Test"
db_host = "127.0.0.1"
db_user = "postgres"
db_passw = "lol123"
passw1 = "Testing1234"
pwdwrong = ["Sorry that's not correct!",
            "Not even close!",
            "Nice Try!",
            "Hold on and give the correct password!"
            ]

def menu():
    while True:
        mspwd = getpass.getpass("\nEnter Your Masterkey: ")
        if mspwd == passw1:
            banner()
            print("Welcome".center(50))
            user_inp = input("\npwm> ")
            if user_inp == "1":
                insert()
            elif user_inp == "3":
                viewDb()
            else:
                return -1
        else:
            print(secrets.choice(pwdwrong))

def banner():
    subprocess.call("clear")
    print("""
+ ================================================== +
|                                                    |
|    1.Add New Credentials                           |                         
|    2.Update Your Existing Credentials              |                 
|    3.View All Your Database                        |
|    4.Search By App Name                            |
|    5.Search By Email                               |    
|    6.Search By Username                            |
|    7.Search By Password                            |
|                                                    |
+ ================================================== +
""")
def encrypt(msg, masterkey):
    masterkey = base64.b64encode(masterkey) 
    IV = os.urandom(16)
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    return base64.b64encode(IV + cipher.encrypt(msg))

def decrypt(encMsg, masterkey):
    masterkey = base64.b64encode(masterkey) 
    encMsg = base64.b64decode(encMsg)
    IV = encMsg[:AES.block_size]
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    return cipher.decrypt(encMsg[AES.block_size:])

def dbconnect():
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_passw, host=db_host)
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Failed to Connect Database", error)


def insert():
    try:
        connection = dbconnect()
        cur = connection.cursor()
        u_name = str(input("Username: "))
        enc = encrypt(getpass.getpass("Password: ").encode(), passw1.encode())
        InsertQuery = f"INSERT INTO users (username, passw) VALUES ('{u_name}', '{enc.decode()}');"
        cur.execute(InsertQuery)
        connection.commit()
        print(f"[+]Successfully Added for {u_name}")
    except (Exception, psycopg2.Error) as error:
        print("Failed to Insert Into Database", error)

    finally:
        if connection:
            connection.close()
            cur.close()
def update(site):
    pass

def searchUser(user):
    pass

def searchPassw(passw):
    pass

def serchMail(mail):
    pass

def viewDb():
    try:
        connection = dbconnect()
        cur = connection.cursor()
        readquery = "SELECT * FROM users;"
        cur.execute(readquery)
        rows = cur.fetchall() 
        connection.commit()
        for row in rows:
            encPass = str(row[2]).encode()
            username = row[1]
            decipher = decrypt(encPass, passw1.encode()).decode()
            print(f"{username} | {decipher}\n")
        
    except (Exception, psycopg2.Error) as error:
        print("Failed to Read Database", error)
    
    finally:
        if connection:
            connection.close()
            cur.close()

menu()
