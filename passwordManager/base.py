
from passwordManager.ciphers import encrypt, decrypt
import sqlite3,base64, getpass
from passwordManager import tools


class DatabaseManager:
    """ Class Doc Goes Here"""

    def __init__(self,MasterPass):
        self.MasterPass = MasterPass

        try:
            self.connection = sqlite3.connect("passwordmanager.db")
            self.cur = self.connection.cursor()

        except Exception as error:
            print("Failed to Connect Database", error , "okaymai")

    

    def viewdb_by_appname(self,APP_NAME):
        
        master_pass = self.MasterPass
        app_name = APP_NAME
        readquery = "SELECT * FROM users WHERE app_name=:app_name;"


        #m_pass = getpass.getpass("MasterKey : ")
        m_pass = "shoaibislam"
        if m_pass == master_pass :
            
            try:
                with self.connection:
                    exs = self.cur.execute(readquery,{"app_name":app_name})
                    rows = self.cur.fetchall() 
            
                content_table = tools.print_box(rows, m_pass)
            
                print(content_table)

            except Exception as error:
                print("Failed to Read Database", error ,"breh")


    def viewdb_by_username(self,UserName):
        
        master_pass = self.MasterPass
        username = UserName
        readquery = "SELECT * FROM users WHERE username=:username;"

        #m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"

        if m_pass == master_pass:
            try:
                with self.connection:
                    self.cur.execute(readquery,{"username":username})
                    rows = self.cur.fetchall() 
                
                content_table = tools.print_box(rows, m_pass)
                print(content_table)
            
            except Exception as error:
                print("Failed to Read Database", error)



    def viewall(self):
        master_pass = self.MasterPass
        readquery = "SELECT * FROM users;"

        # m_pass = getpass.getpass("MasterKey: ")
        m_pass = "shoaibislam"
        
        if m_pass == master_pass :
            try:
                
                with self.connection:

                    self.cur.execute(readquery)
                    rows = self.cur.fetchall() 
                
                content_table = tools.print_box(rows, m_pass)
                print(content_table)
            
            except Exception as error:
                print("Failed to Read Database", error)
     

    def insert(self,AppName=None,UserName=None):

        master_pass= self.MasterPass
        InsertQuery = f"INSERT INTO users (app_name,username, passw) VALUES (:appname ,:u_name,:pass)"
            
        #m_pass = getpass.getpass("MasterKey: ")

        m_pass = "shoaibislam"

        if m_pass == master_pass:

            app_name = str(input("app_name :"))
            u_name = str(input("Username: "))
            enc = encrypt(getpass.getpass("Password: ").encode(), m_pass.encode())
            
            try: 

                with self.connection:
                    self.cur.execute(InsertQuery,{
                        "appname": app_name,
                        "u_name":u_name,
                        "pass":enc.decode()
                    }
                    )
                
                
                print(f"[+]Successfully Added for {u_name}")


            except Exception as error:
                print("Failed to Insert Into Database", error)
