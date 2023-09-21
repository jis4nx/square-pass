from sqpass.passwordManager.ciphers import encrypt, decrypt
from sqpass.passwordManager import tools

from prettytable import PrettyTable
from contextlib import contextmanager
import sqlite3
import getpass
import sys
import os
import base64
import platform
import json


home_dir = os.path.expanduser("~")
db_path = os.path.join(home_dir, ".local", "share", "pass.db")

paths = {
    'Linux': os.path.expanduser("~/.local/share/pass.key"),
    'Windows': os.path.expanduser("~\\AppData\\pass.key")
}
pathname = paths.get(platform.system())


def readpass():
    if not os.path.exists(pathname):
        print('No Passkey found\nPerhaps you forgot to execute `sq-init`')
    else:
        with open(pathname, "r") as file:
            return file.read()


class DatabaseManager:
    """ Class Doc Goes Here"""

    def __init__(self, MasterPass, cryptedpass):
        self.User_Masterpass = readpass()
        check_pass = True if self.User_Masterpass == cryptedpass else False
        self.cryptedpass = cryptedpass if check_pass else None
        self.MasterPass = MasterPass if check_pass else None
        self.db = db_path
        if not check_pass:
            print("Not matched")
        try:
            self.termlines = os.get_terminal_size().columns
        except Exception:
            self.termlines = 100

    @contextmanager
    def opendb(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        try:
            yield cur
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            raise
        finally:
            conn.commit()
            conn.close()

    @contextmanager
    def dbfetch(self, query, data=None):
        try:
            conn = sqlite3.connect(self.db)
            cur = conn.cursor()
            if data is None:
                cur.execute(query)
            else:
                cur.execute(query, data)
            yield cur.fetchall()
        except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
            print("Database not found, Try to run `sq-init`")
            exit()
        finally:
            cur.close()

    def update(self, table='passw', id=None):
        local_pass = self.MasterPass
        if self.cryptedpass == self.User_Masterpass:
            if table == "passw":
                lst = ["app_name", "username", "passwd"]
                lstinp = ["App Name: ", "Username: ", "Password: "]
            else:
                lst = ["title", "key"]
                lstinp = ["Title: ", "Key: "]
            userinp = []

            for idxlst, inp in enumerate(lst):
                if inp == "passwd":
                    salt, iv, enc = encrypt(getpass.getpass("Password: ").encode(
                        'utf-8'), local_pass.encode('utf-8'))
                    enc = json.dumps({'salt': salt, 'iv': iv, 'enc': enc})
                else:
                    enc = input(lstinp[idxlst])
                userinp.append(enc)

            for idx, inp in enumerate(userinp):
                if inp != "":
                    try:
                        with self.opendb() as cur:
                            update_query = f"""UPDATE '{table}'
                                                SET '{lst[idx]}' = '{inp}'
                                                WHERE id={id};"""
                            cur.execute(update_query)
                    except sqlite3.Error as err:
                        print(err)
                else:
                    pass

    def count(self, icase=False, table=None, column=None, cred=None):
        if self.cryptedpass != self.User_Masterpass:
            return

        if column == "passwd":
            passlist = self._get_decrypted_passwords()
            self._print_passwords(passlist, cred)
        else:
            readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}';"
            if icase:
                readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}' COLLATE NOCASE;"
            with self.dbfetch(readquery.format(table, column, cred)) as row:
                if row:
                    print(row[0][0])

    def _get_decrypted_passwords(self):
        local_pass = self.MasterPass
        passlist = []
        with self.dbfetch("SELECT username, app_name, passwd FROM passw;") as row:
            if row:
                for col in row:
                    data = json.loads(col[2])
                    salt, iv, ct = data.values()
                    decipher = decrypt(
                        salt, iv, ct, local_pass.encode()).decode()
                    passlist.append(
                        {'Username': col[0], 'App': col[1], 'Pass': decipher})
        return passlist

    def _print_passwords(self, passlist, cred):
        headers = ['Username', 'App Name', 'Password']
        t = PrettyTable(headers)
        count = 0
        for passw in passlist:
            print()
            if cred == passw['Pass']:
                count += 1
                t.add_row([passw['Username'], passw['App'], passw['Pass']])
        col = ['' for _ in range(count-1)]
        t.add_column("Count", [str(count), *col])
        print(t)

    def filter(self, icase=False, username=None, appname=None, state="OR"):
        if username is None and appname is None:
            print("Please Define A Service Parameter")
        elif username is not None or appname is not None:
            local_pass = self.MasterPass
            if icase:
                readquery = """SELECT * FROM passw WHERE username = '{}' COLLATE NOCASE {} app_name = '{}' COLLATE NOCASE;"""
            else:
                readquery = """SELECT * FROM passw WHERE username = '{}' {} app_name = '{}';"""
            with self.dbfetch(readquery.format(username, state, appname)) as row:
                if row:
                    tools.print_box(row, local_pass)

    def view_notes(self, sort="id", order="ASC", markdown=False, noteid=None):
        if self.cryptedpass == self.User_Masterpass:
            if noteid is None:
                readquery = f"SELECT * FROM notes ORDER BY {sort} {order};"
            else:
                readquery = f"SELECT * FROM notes WHERE id={noteid};"
            if self.cryptedpass == self.User_Masterpass:
                with self.dbfetch(readquery) as row:
                    if row:
                        if noteid is None:
                            notes = PrettyTable()
                            notes.field_names = ["Index", "Title", "Content"]
                            for idx, title, cont, dtime in row:
                                notes.add_row(
                                    [idx, title, base64.b64decode(cont).decode()[:10]+"..."])
                            print(notes)

                        else:
                            try:
                                title = row[0][1]
                                content = (
                                    (base64.b64decode(row[0][2])).decode()).strip()
                                subtitle = row[0][3]

                                tools.print_note(content, title, subtitle)
                            except IndexError:
                                print("Not Available")

    def view_keys(self, sort="id", order="ASC", keyid=None, export=False):
        local_pass = self.MasterPass
        if keyid is None:
            readquery = f"SELECT * FROM keys ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM keys WHERE id = {keyid};"
        if self.cryptedpass == self.User_Masterpass:
            with self.dbfetch(readquery) as row:
                if row and len(row) < 1:
                    print("Not Available")
                else:
                    keys = PrettyTable()
                    keys.field_names = ["Index", "Title", "Key"]
                    for r in row:
                        data = json.loads(r[2])
                        salt, iv, ct = data.values()
                        decipher = decrypt(
                            salt, iv, ct, local_pass.encode()).decode()
                        keys.add_row([r[0], r[1], decipher])
                    if export:
                        return keys
                    print(keys)

    def view_userpasses(self, sort="id", order="ASC", userid=None, countpass=False, export=False):
        if userid is None:
            readquery = f"SELECT * FROM passw ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM passw WHERE id = {userid};"
        local_pass = self.MasterPass
        if self.cryptedpass == self.User_Masterpass:
            with self.dbfetch(readquery) as row:
                if row:
                    content_table = tools.print_box(row, local_pass)
                    if export:
                        return content_table
                    print(content_table)

    def insert(self, app_name=None, user_name=None):  # Pylint: disable=W0613
        insert_query = """INSERT INTO passw (app_name,username, passwd)
                            VALUES (:appname ,:u_name,:passw)"""
        local_pass = self.MasterPass
        if self.cryptedpass == self.User_Masterpass:
            app_name = input("App Name:")
            u_name = input("Username: ")
            salt, iv, enc = encrypt(getpass.getpass("Password: ").encode(
                'utf-8'), local_pass.encode('utf-8'))
            data = json.dumps({'salt': salt, 'iv': iv, 'enc': enc})

            try:
                with self.opendb() as cur:
                    cur.execute(insert_query, {
                        "appname": app_name,
                        "u_name": u_name,
                        "passw": data
                    }
                    )
                print(f"[+]Successfully Added for {u_name}")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)

    def keyins(self, title=None, silent=True):  # Pylint: disable=W0613
        insert_query = """INSERT INTO keys (title, key)
                            VALUES (:key_title ,:key_pass)"""
        local_pass = self.MasterPass
        if self.cryptedpass == self.User_Masterpass:
            if title is None:
                title = input("Title: ")
            if silent:
                salt, iv, enc = encrypt(getpass.getpass(
                    "Key: ").encode(), local_pass.encode())
                data = json.dumps({'salt': salt, 'iv': iv, 'enc': enc})
            else:
                salt, iv, enc = encrypt(
                    input("Key: ").encode(), local_pass.encode())
                data = json.dumps({'salt': salt, 'iv': iv, 'enc': enc})
            try:
                with self.connection:
                    self.cur.execute(insert_query, {
                        "key_title": title,
                        "key_pass": data
                    }
                    )
                print()
                print(f"[+]Stored Key for {title}")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)

    def noteins(self, title=None):  # Pylint: disable=W0613
        insert_query = """INSERT INTO notes (title,content, date)
                            VALUES (:note_title ,:note_content, datetime())"""
        if self.cryptedpass == self.User_Masterpass:
            if title is None:
                title = input("Title:")
            centext = "BODY"
            save_text = " [CTRL + D] "
            discard = " [CTRL + C] "

            eq = (self.termlines//2)-(len(save_text+centext+discard)//2)
            last_put = " "*(eq)+centext+" "*(eq)
            print("_"*self.termlines)
            print(discard, end="")
            print(last_put, end="")
            print(save_text, end="")
            print("-"*self.termlines)

            note_content = "".join(sys.stdin.readlines())
            contb64 = base64.b64encode(note_content.encode())
            try:
                with self.connection:
                    self.cur.execute(insert_query, {
                        "note_title": title,
                        "note_content": contb64,
                    }
                    )
                print()
                print(f"[+]Note Added")
            except sqlite3.Error as error:
                print("Failed to Insert Into Database", error)

    def remove_cd(self, table=None, u_id=None):

        query = f"DELETE FROM {table} WHERE id={u_id}"

        with self.connection:
            self.cur.execute(query)

    def bigbang(self, boom=False, userpass=None, keys=None, notes=None):
        master_pass = self.MasterPass
        if boom:
            userpass = True
            keys = True
            notes = True
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

    def export(self, service=None, json=False, csv=False):
        backup = ""
        ext = ".json" if json else ".csv"
        if self.cryptedpass == self.User_Masterpass:
            if service == "passw":
                rawbac = self.view_userpasses(export=True)
                backup = rawbac.get_json_string() if json else rawbac.get_csv_string()

            elif service == "keys":
                rawbac = self.view_keys(export=True)
                backup = rawbac.get_json_string() if json else rawbac.get_csv_string()
            else:
                print("service name was not found")
            print(backup)
            with open("backup"+ext, "w") as f:
                for line in backup:
                    if line != "\n":
                        f.write(line)
