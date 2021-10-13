
#import psycopg
#from Crypto.Cipher import AES
import getpass
import sqlite3
import base64
import os,subprocess, getpass, secrets
from passwordManager.ciphers import encrypt, decrypt

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
            input()
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



def print_as_box(app_name,username,passes):
    total =  len(app_name)+len(username)+len(paisses)
    box_shade = "="*(  int(total)+10 )
    box = box_shade
    print(box_shade)













def viewdb_by_appname():
    passw1 = "shoaibislam"
    try:
        connection = dbconnect()
        cur = connection.cursor()


        username_inp = input("input app_name : ")
        readquery = "SELECT * FROM users WHERE username=:username_inp;"

        with connection:

            cur.execute(readquery,{"username_inp":username_inp})
            rows = cur.fetchall() 
            
            for row in rows:
                encPass = str(row[2]).encode()
                username = row[1]
                app_name = row[0]
                decipher = decrypt(encPass, passw1.encode()).decode()
                box="======================================="
                print(box)
                print(f" {app_name} |{username} | {decipher}\n")
            input()
    except Exception as error:
        print("Failed to Read Database", error)
    




def viewdb_by_username():
    passw1 = "shoaibislam"
    try:
        connection = dbconnect()
        cur = connection.cursor()


        usr_app_inp = input("input app_name : ")
        readquery = "SELECT * FROM users WHERE app_name=:usr_app_inp;"

        with connection:

            cur.execute(readquery,{"usr_app_inp":usr_app_inp})
            rows = cur.fetchall() 
            
            for row in rows:
                encPass = str(row[2]).encode()
                username = row[1]
                app_name = row[0]
                decipher = decrypt(encPass, passw1.encode()).decode()
                box="======================================="
                print(box)
                print(f" {app_name} |{username} | {decipher}\n")
            input()
    except Exception as error:
        print("Failed to Read Database", error)
    















def viewDb():
    passw1 = "shoaibislam"
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
                decipher = decrypt(encPass, passw1.encode()).decode()
                box="======================================="
                print(box)
                print(f" {app_name} |{username} | {decipher}\n")
            input()
    except Exception as error:
        print("Failed to Read Database", error)
    


