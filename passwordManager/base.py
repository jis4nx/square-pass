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
        try:
            self.termlines = os.get_terminal_size().columns
        except:
            self.termlines = 100

    
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


    def update(self,table="users", row=None, value=None, id=None):
        master_pass = self.MasterPass
        m_pass = "shoaibislam"

        if table == "users":
            lst = ["app_name", "username", "passw"]
        else:
            lst = ["title", "key"]
        userinp = []


        for inp in lst:
            if inp == "passw":
                enc = encrypt(getpass.getpass(str(inp)).encode(), m_pass.encode()).decode()
            else:
                enc = input(str(inp))
            userinp.append(enc)


        for idx, inp in enumerate(userinp):
            if inp != "":
                try:
                    with self.connection:
                        # self.cur.execute(update_query.format(table, lst[idx], fr"{inp}", id))
                        update_query = f"""UPDATE {table}
                                            SET {lst[idx]} = '{inp}', date=datetime()
                                        WHERE id={id};"""
                        self.cur.execute(update_query)
                except sqlite3.Error as err:
                    print(err)
            else:
                pass

  
    def viewdb_base(self,username=None,appname=None,state="or"):

            if username is None and appname is None:
                # self.viewall()
                print("Please Define A Service Parameter")

            elif username is not None or appname is not None:
                
                master_pass = self.MasterPass
                readquery = f"SELECT * FROM users WHERE username=:user_name {state} app_name=:appname;"
            
                m_pass = "shoaibislam"
                user_dict = {"user_name":username,"appname":appname}
                if m_pass == master_pass:
                    row = self.dbfetch(readquery, user_dict)
                    content_table = tools.print_box(row, m_pass)
                    print(content_table)


    def view_notes(self,sort="id",order="ASC"):
        master_pass = self.MasterPass
        readquery = f"SELECT * FROM notes ORDER BY {sort} {order};"
        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            for w,x,y,z in row:
                print("|",w,"|",x,"|",(base64.b64decode(y).decode()).strip(),"|")

    
    def view_keys(self, sort="id", order="ASC"):
        master_pass = self.MasterPass
        readquery = f"SELECT * FROM keys ORDER BY {sort} {reverse};"
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            print("-"*40)
            # print(x,"|",y)


    def view_userpasses(self, sort="id", order="ASC"):
        master_pass = self.MasterPass
        readquery = f"SELECT * FROM users ORDER BY {sort} {order};"
        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            content_table = tools.print_box(row, m_pass)
            print(content_table)


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
        insert_query = """INSERT INTO notes (title,content, date)
                            VALUES (:note_title ,:note_content, datetime())"""
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



    def bigbang(self,boom=False, userpass=None, keys=None, notes=None):
        master_pass = self.MasterPass
        if boom:
            userpass=True
            keys=True
            notes=True
        query = """DELETE FROM {}"""
        if userpass is not None:
            with self.connection:
                self.cur.execute(query.format("users"))
        if keys is not None:
            with self.connection:
                self.cur.execute(query.format("keys"))
        if notes is not None:
            with self.connection:
                self.cur.execute(query.format("notes"))
        
