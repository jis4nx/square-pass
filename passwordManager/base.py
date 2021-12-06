import sqlite3
import getpass
from passwordManager.ciphers import encrypt
from passwordManager import tools


class DatabaseManager:
    """ Class Doc Goes Here"""

    def __init__(self,MasterPass):
        self.MasterPass = MasterPass
        self.connection = sqlite3.connect("passwordmanager.db")
        self.cur = self.connection.cursor()

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

    def viewdb_by_appname(self,APP_NAME):
            master_pass = self.MasterPass
            app_name = APP_NAME
            readquery = "SELECT * FROM users WHERE app_name=:app_name;"
            m_pass = "shoaibislam"
            app_dict = {"app_name":app_name}
            if m_pass == master_pass :
                row = self.dbfetch(readquery, app_dict)
                content_table = tools.print_box(row, m_pass)
                print(content_table)

    def viewdb_by_username(self,user_name):
            master_pass = self.MasterPass
            readquery = "SELECT * FROM users WHERE username=:user_name;"
            m_pass = "shoaibislam"
            user_dict = {"user_name":user_name}
            if m_pass == master_pass:
                row = self.dbfetch(readquery, user_dict)
                content_table = tools.print_box(row, m_pass)
                print(content_table)

    def viewall(self):
        master_pass = self.MasterPass
        readquery = "SELECT * FROM users;"
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
