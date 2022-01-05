import sqlite3
import getpass
import sys
import os
import base64
from passwordManager.ciphers import encrypt,decrypt
from passwordManager import tools
from prettytable import PrettyTable

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


    def update(self,table="passw", row=None, value=None, id=None):
        master_pass = self.MasterPass
        m_pass = "shoaibislam"

        if table == "passw":
            lst = ["app_name", "username", "passwd"]
            lstinp = ["App Name: ", "Username: ", "Password: "]
        else:
            lst = ["title", "key"]
            lstinp = ["Title: ", "Key: "]
        userinp = []


        for idxlst, inp in enumerate(lst):
            if inp == "passwd":
                inpass = getpass.getpass(lstinp[idxlst])
                enc = encrypt(getpass.getpass(lstinp[idxlst]).encode(), m_pass.encode()).decode() if inpass != "" else ""

            else:
                enc = input(lstinp[idxlst])
            userinp.append(enc)


        for idx, inp in enumerate(userinp):
            if inp != "":
                try:
                    with self.connection:
                        update_query = f"""UPDATE {table}
                                            SET {lst[idx]} = '{inp}', date=datetime()
                                        WHERE id={id};"""
                        self.cur.execute(update_query)
                except sqlite3.Error as err:
                    print(err)
            else:
                pass

  
    def count(self,icase=False, table=None, column=None, cred=None):
        master_pass = self.MasterPass
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}';"
            try:
                if column == "passwd":
                    passlist = []
                    row = self.dbfetch("SELECT passwd FROM passw;")
                    for x in row:
                        decipher = decrypt(x[0], master_pass.encode()).decode()
                        passlist.append(decipher)
                    print(passlist.count(cred))

                else:
                    if icase:
                        readquery = "SELECT COUNT(*) FROM {} WHERE {} = lower('{}');"
                    else:
                        readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}';"
                    row = self.dbfetch(readquery.format(table, column, cred))
                    print(row[0][0])

            except Exception as err:
                print(err)
                

    def filter(self,icase=False,username=None,appname=None,state="or"):
        if username is None and appname is None:
            print("Please Define A Service Parameter")
        elif username is not None or appname is not None:
            master_pass = self.MasterPass
            m_pass = "shoaibislam"
            if icase:
                readquery = """SELECT * FROM passw WHERE username = lower('{}') {} app_name = lower('{}');"""
            else:
                readquery = """SELECT * FROM passw WHERE username = '{}' {} app_name = '{}';"""
                # user_dict = {"user_name":username,"appname":appname}
            row = self.dbfetch(readquery.format(username, state, appname))
            content_table = tools.print_box(row, m_pass)
            print(content_table)



    def view_notes(self,sort="id",order="ASC" ,markdown=False,noteid=None):
        master_pass = self.MasterPass

        if noteid is None :
            readquery = f"SELECT * FROM notes ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM notes WHERE id={noteid};"
        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            if noteid == None:
                notes = PrettyTable()
                notes.field_names = ["Index", "Title", "Content"]
                for idx,title,cont,dtime in row:
                    notes.add_row([idx, title, base64.b64decode(cont).decode()[:10]+"..."])
                print(notes)

            else:
                try:
                    magicnum = row[0][0] 
                    title = row[0][1]
                    content = ((base64.b64decode(row[0][2])).decode()).strip()
                    subtitle= row[0][3]
                    
                    tools.print_note(content,title,subtitle)
                except IndexError:
                    print("Not Available")


                 
    def view_keys(self, sort="id", order="ASC",keyid=None):
        master_pass = self.MasterPass
        if keyid is None:
            readquery = f"SELECT * FROM keys ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM keys WHERE id = {keyid};"
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            if len(row) < 1:
                print("Not Available")
            else:
                keys = PrettyTable()
                keys.field_names = ["Index", "Title", "Key"]
                for r in row:
                    decipher = decrypt(r[2], master_pass.encode()).decode()
                    keys.add_row([r[0], r[1], decipher])
                keys.sortby = "Key"
                print(keys)


    def view_userpasses(self, sort="id", order="ASC", userid=None, countpass=False):
        master_pass = self.MasterPass
        if userid is None:
            readquery = f"SELECT * FROM passw ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM passw WHERE id = {userid};"
        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            row = self.dbfetch(readquery)
            content_table = tools.print_box(row, m_pass)
            print(content_table)

    def insert(self,app_name=None,user_name=None): # Pylint: disable=W0613
        master_pass= self.MasterPass
        insert_query = """INSERT INTO passw (app_name,username, passwd)
                            VALUES (:appname ,:u_name,:pass)"""
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            app_name = input("App Name:")
            u_name = input("Username: ")
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


    def keyins(self, title=None, silent=True): # Pylint: disable=W0613
        master_pass= self.MasterPass
        insert_query = """INSERT INTO keys (title, key)
                            VALUES (:key_title ,:key_pass)"""
        m_pass = "shoaibislam"
        if m_pass == master_pass:
            if title is None:
                title = input("Title: ")
            if silent:
                enc = encrypt(getpass.getpass("Key: ").encode(), m_pass.encode())
            else:
                enc = encrypt(input("Key: ").encode(), m_pass.encode())
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


    def remove_cd(self,table=None,u_id=None):
        
        query = f"DELETE FROM {table} WHERE id={u_id}"

        with self.connection:
            self.cur.execute(query)



    def bigbang(self,boom=False, userpass=None, keys=None, notes=None):
        master_pass = self.MasterPass
        if boom:
            userpass=True
            keys=True
            notes=True
        query = """DELETE FROM {}"""
        if userpass is not None:
            with self.connection:
                self.cur.execute(query.format("passw"))
        if keys is not None:
            with self.connection:
                self.cur.execute(query.format("keys"))
        if notes is not None:
            with self.connection:
                self.cur.execute(query.format("notes"))
        


