
from passwordManager.ciphers import encrypt, decrypt
import sqlite3,base64, getpass





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
            
            #InsertQuery = f"INSERT INTO users (username, passw) VALUES ('{u_name}', '{enc.decode()}');"/
        
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


            #username_inp = input("input app_name : ")
            app_name = APP_NAME

            readquery = "SELECT * FROM users WHERE app_name=:app_name;"

            with connection:

                cur.execute(readquery,{"app_name":app_name})
                rows = cur.fetchall() 
                for row in rows:
                    encPass = str(row[2]).encode()
                    username = row[1]
                    app_name = row[0]
                    decipher = decrypt(encPass, master_pass.encode()).decode()
                    box="======================================="
                    print(box)
                    print(f" {app_name} |{username} | {decipher}\n")
                    #print_as_box

            print(m_pass)
            
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
                
                for row in rows:
                    encPass = str(row[2]).encode()
                    username = row[1]
                    app_name = row[0]
                    decipher = decrypt(encPass, master_pass.encode()).decode()
                    box="======================================="
                    print(box)
                    print(f" {app_name} |{username} | {decipher}\n")
                input()
        except Exception as error:
            print("Failed to Read Database", error)
    




def viewall(MASTERPASS):
    master_pass = MASTERPASS

    m_pass = getpass.getpass("MasterKey: ")
    
    if m_pass == master_pass :

        try:
            connection = dbconnect()
            cur = connection.cursor()
            readquery = "SELECT * FROM users;"

            with connection:

                cur.execute(readquery)
                rows = cur.fetchall() 
                
                for row in rows:
                    encPass = str(row[2]).encode()
                    username = row[1]
                    app_name = row[0]
                    decipher = decrypt(encPass, master_pass.encode()).decode()
                    box="======================================="
                    print(box)
                    print(f" {app_name} |{username} | {decipher}\n")
    
        except Exception as error:
            print("Failed to Read Database", error)
    

