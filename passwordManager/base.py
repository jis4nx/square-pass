import sqlite3
import getpass
from passwordManager.ciphers import encrypt
from passwordManager import tools
import base64
import sys
import os


class DatabaseManager:
    """ Class Doc Goes Here"""

    def __init__(self,MasterPass):
        self.MasterPass = MasterPass
        self.connection = sqlite3.connect("passwordmanager.db")
        self.cur = self.connection.cursor()
        self.termlines = os.get_terminal_size().columns

    def dbfetch(self, query, dict=None):
            try:
                with self.connection:
                    if dict is None:
                        self.cur.execute(query)
                    else:
                        self.cur.execute(query, dict)
                    return self.cur.fetchall()
            except sqlite3.Error as err:
                print(err)

    # def viewdb_by_appname(self,APP_NAME):
            # master_pass = self.MasterPass
            # app_name = APP_NAME
            # readquery = "SELECT * FROM users WHERE app_name=:app_name;"
            # m_pass = "shoaibislam"
            # app_dict = {"app_name":app_name}
            # if m_pass == master_pass :
                # row = self.dbfetch(readquery, app_dict)
                # content_table = tools.print_box(row, m_pass)
                # print(content_table)

    # def viewdb_by_username(self,user_name):
            # master_pass = self.MasterPass
            # readquery = "SELECT * FROM users WHERE username=:user_name;"
            # m_pass = "shoaibislam"
            # user_dict = {"user_name":user_name}
            # if m_pass == master_pass:
                # row = self.dbfetch(readquery, user_dict)
                # content_table = tools.print_box(row, m_pass)
                # print(content_table)

  
    def viewdb_base(self,username=None,appname=None,state="or"):

            if username is None and appname is None:
                self.viewall()

            elif username is not None or appname is not None:
                
                master_pass = self.MasterPass
                readquery = f"SELECT * FROM users WHERE username=:user_name {state} app_name=:appname;"
            
                m_pass = "shoaibislam"
                user_dict = {"user_name":username,"appname":appname}
                if m_pass == master_pass:
                    row = self.dbfetch(readquery, user_dict)
                    content_table = tools.print_box(row, m_pass)
                    print(content_table)


    def viewall(self):
        master_pass = self.MasterPass
        readquery = "SELECT * FROM notes;"
        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            # content_table = tools.print_box(row, m_pass) 
            title = row[-1][0] 
            note = base64.b64decode( (row[-1][1] )).decode()
            # print(title)

            tools.print_note(str(note),str(title))
            # for x, y in row:
                # print(x, base64.b64decode(y).decode())

    

    def insert(self,app_name=None,user_name=None): # Pylint: disable=W0613
        master_pass= self.MasterPass
        insert_query = """INSERT INTO users (app_name,username, passw)
                            VALUES (:appname ,:u_name,:pass)"""
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            app_name = str(input("app_name :"))
            u_name = str(input("Username: "))
            enc = encrypt(getpass.getpass("Password: ").encode(), m_pass.encode())
            try:
                with self.connection:
                    self.cur.execute(insert_query,{
                        "appname": app_name,
                        "u_name":u_name,
                        "pass":enc.decode()
                    }
                    )
                print(f"[+]Successfully Added for {u_name}")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)


    def keyins(self, title=None): # Pylint: disable=W0613
        master_pass= self.MasterPass
        insert_query = """INSERT INTO keys (title, key)
                            VALUES (:key_title ,:key_pass)"""
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            if title is None:
                title = input("Title :")
            enc = encrypt(getpass.getpass("Key: ").encode(), m_pass.encode())
            try:
                with self.connection:
                    self.cur.execute(insert_query,{
                        "key_title": title,
                        "key_pass":enc.decode()
                    }
                    )
                print()
                print(f"[+]Stored Key for {title}")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)

    def noteins(self, title=None): # Pylint: disable=W0613
        master_pass= self.MasterPass
        insert_query = """INSERT INTO notes (title,content)
                            VALUES (:note_title ,:note_content)"""
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            if title is None:
                title = input("Title:")

            

            centext = "BODY"
            save_text = " [CTRL + D] "
            discard = " [CTRL + C] "

            eq = (self.termlines//2)-(len(save_text+centext+discard)//2)
            last_put = " "*(eq)+centext+" "*(eq)

            print("_"*self.termlines)
           
            print(discard,end="")
            print(last_put,end="")
            print(save_text,end="")

            print("-"*self.termlines)




            note_content = "".join(sys.stdin.readlines())
            contb64 = base64.b64encode(note_content.encode())
            try:
                with self.connection:
                    self.cur.execute(insert_query,{
                        "note_title": title,
                        "note_content": contb64,
                    }
                    )
                print()
                print(f"[+]Note Added")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)
