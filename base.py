
import psycopg
import sqlite3



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


