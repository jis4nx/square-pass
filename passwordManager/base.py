
#import psycopg
from Crypto.Cipher import AES
import getpass
import sqlite3
import base64
import os,subprocess, getpass, secrets


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
        conn = sqlite3.connect("passwordmanager.db")
        return conn
    except Exception as error:
        print("Failed to Connect Database", error)


def insert():
    try:
        passw1 = "shoaibislam"
        connection = dbconnect()
        cur = connection.cursor()
        app_name = str(input("app_name :"))
        u_name = str(input("Username: "))
        enc = encrypt(getpass.getpass("Password: ").encode(), passw1.encode())
        
        #InsertQuery = f"INSERT INTO users (username, passw) VALUES ('{u_name}', '{enc.decode()}');"/
    
        with connection:
            InsertQuery = f"INSERT INTO users (app_name,username, passw) VALUES (:appname ,:u_name,:pass)"
            cur.execute(InsertQuery,{
                "appname": app_name,
                "u_name":u_name,
                "pass":enc.decode()
            })
        
            print(f"[+]Successfully Added for {u_name}")
    except Exception as error:
        print("Failed to Insert Into Database", error)

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


