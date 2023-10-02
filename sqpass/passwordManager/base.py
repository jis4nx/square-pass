from sqpass.create_db import clear_db
from sqpass.passwordManager.ciphers import encrypt, decrypt
from sqpass.passwordManager import tools
from sqpass.passwordManager.tools import opendb, dbfetch
from prettytable import PrettyTable
import sqlite3
import getpass
import sys
import os
import base64
import json
from sqpass.install import password_path
from sqpass.create_db import db_path


def readpass():
    if not os.path.exists(password_path):
        print("No Passkey found\nPerhaps you forgot to execute `sq-init`")
    else:
        with open(password_path, "r") as file:
            return file.read()


class DatabaseManager:
    """Class Doc Goes Here"""

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

    def update(self, table="passw", id=None):
        """Updates a record in the database.

        Args:
            table: The name of the table to update.
            id: The ID of the record to update.
        """

        columns = {
            "passw": ["app_name", "username", "passwd"],
            "default": ["title", "key"],
        }

        prompts = {
            "passw": ["App Name: ", "Username: ", "Password: "],
            "default": ["Title: ", "Key: "],
        }

        user_inputs = []
        for col_id, column in enumerate(columns[table]):
            if column == "passwd":
                password = getpass.getpass("Password: ")
                if password:
                    salt, iv, enc = encrypt(
                        password.encode(
                            "utf-8"), self.MasterPass.encode("utf-8")
                    )
                    enc = json.dumps({"salt": salt, "iv": iv, "enc": enc})
                    user_inputs.append(enc)
            else:
                user_inputs.append(input(prompts[table][col_id]))

        try:
            with opendb(self.db) as cur:
                for idx, inp in enumerate(user_inputs):
                    if inp != "":
                        update_query = f"""UPDATE '{table}' SET '{columns[table][idx]}' = :inp WHERE id=:id;"""
                        cur.execute(update_query, {"inp": inp, "id": id})
                print("[+] Updated")
        except sqlite3.Error as err:
            print(err)

    def count(self, icase=False, table=None, column=None, cred=None):
        """Counts the number of rows in a table that match a given condition.

        Args:
          icase: Whether to perform a case-insensitive comparison.
          table: The name of the table to count rows from.
          column: The name of the column to filter by.
          cred: The credential to use to connect to the database.

        Returns:
          The number of rows that match the given condition.
        """

        if column == "passwd":
            passlist = self._get_decrypted_passwords()
            self._print_passwords(passlist, cred)
            return

        readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}';"
        if icase:
            readquery = "SELECT COUNT(*) FROM {} WHERE {} = '{}' COLLATE NOCASE;"
        with dbfetch(self.db, readquery.format(table, column, cred)) as row:
            if row:
                return row[0][0]
        return 0

    def _get_decrypted_passwords(self):
        passlist = []
        with dbfetch(self.db, "SELECT username, app_name, passwd FROM passw;") as row:
            if row:
                for col in row:
                    data = json.loads(col[2])
                    salt, iv, ct = data.values()
                    decipher = decrypt(
                        salt, iv, ct, self.MasterPass.encode()).decode()
                    passlist.append(
                        {"Username": col[0], "App": col[1], "Pass": decipher}
                    )
        return passlist

    def _print_passwords(self, passlist, cred):
        headers = ["Username", "App Name", "Password"]
        t = PrettyTable(headers)
        count = 0
        for passw in passlist:
            print()
            if cred == passw["Pass"]:
                count += 1
                t.add_row([passw["Username"], passw["App"], passw["Pass"]])
        col = ["" for _ in range(count - 1)]
        t.add_column("Count", [str(count), *col])
        print(t)

    def filter(self, icase=False, username=None, appname=None, state="OR"):
        """
        Filters (username or password or both) from `passw` table

        Args:
            icase: For case-insensitive -> boolean
            username: Username for passw table -> string
            appname: App Name for passw table -> string
        """
        if username is None and appname is None:
            print("Please Define A Service Parameter")
        elif username is not None or appname is not None:
            if icase:
                readquery = """SELECT * FROM passw WHERE username = '{}' COLLATE NOCASE {} app_name = '{}' COLLATE NOCASE;"""
            else:
                readquery = (
                    """SELECT * FROM passw WHERE username = '{}' {} app_name = '{}';"""
                )
            with dbfetch(self.db, readquery.format(username, state, appname)) as row:
                if row:
                    tools.print_box(row, self.MasterPass)

    def view_notes(self, sort="id", order="ASC", markdown=False, indexId=None):
        """
        View notes from the database.

        Args:
            sort: The column to sort by index [primary key] -> int
            order: The order to sort by Ascending or Descending -> string
            markdown: Whether to render the note content in Markdown -> bool
            indexId: The ID of the specific note to view -> int
        """

        readquery = f"SELECT * FROM notes ORDER BY {sort} {order};"
        if indexId is not None:
            readquery = f"SELECT * FROM notes WHERE id={indexId};"

        with dbfetch(self.db, readquery) as row:
            if row:
                if indexId is None:
                    notes = PrettyTable()
                    notes.field_names = ["Index", "Title", "Content"]
                    for idx, title, cont, dtime in row:
                        notes.add_row(
                            [idx, title, base64.b64decode(
                                cont).decode()[:10] + "..."]
                        )
                    print(notes)
                else:
                    try:
                        title = row[0][1]
                        content = base64.b64decode(row[0][2]).decode().strip()
                        subtitle = row[0][3]

                        tools.print_note(content, title, subtitle, markdown)
                    except IndexError:
                        print("Not Available")

    def view_keys(self, sort="id", order="ASC", indexId=None, export=False):
        """
        Retrieve all Keys from `keys` table

        Args:
            sort: Sort by id [primary key] -> string
            order: Ascending or Descending -> string
            indexId: Index key of the table -> integer
            export: " -> boolean"
        """
        if indexId is None:
            readquery = f"SELECT * FROM keys ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM keys WHERE id = {indexId};"
        with dbfetch(self.db, readquery) as row:
            if row and len(row) < 1:
                print("Not Available")
            else:
                keys = PrettyTable()
                keys.field_names = ["Index", "Title", "Key"]
                for r in row:
                    data = json.loads(r[2])
                    salt, iv, ct = data.values()
                    decipher = decrypt(
                        salt, iv, ct, self.MasterPass.encode()).decode()
                    keys.add_row([r[0], r[1], decipher])
                if export:
                    return keys
                print(keys)

    def view_userpasses(
        self, sort="id", order="ASC", indexId=None, countpass=False, export=False
    ):
        if indexId is None:
            readquery = f"SELECT * FROM passw ORDER BY {sort} {order};"
        else:
            readquery = f"SELECT * FROM passw WHERE id = {indexId};"
        with dbfetch(self.db, readquery) as row:
            if row:
                content_table = tools.print_box(row, self.MasterPass)
                if export:
                    return content_table
                print(content_table)

    def insert(self, app_name=None, user_name=None):  # Pylint: disable=W0613
        insert_query = """INSERT INTO passw (app_name,username, passwd)
                            VALUES (:appname ,:u_name,:passw)"""
        app_name = input("App Name:")
        u_name = input("Username: ")
        salt, iv, enc = encrypt(
            getpass.getpass("Password: ").encode("utf-8"),
            self.MasterPass.encode("utf-8"),
        )
        data = json.dumps({"salt": salt, "iv": iv, "enc": enc})

        try:
            with opendb(self.db) as cur:
                cur.execute(
                    insert_query, {"appname": app_name,
                                   "u_name": u_name, "passw": data}
                )
            print(f"[+]Successfully Added for {u_name}")
        except sqlite3.Error as error:
            print("Failed to Insert Into Database", error)

    def keyins(self, title=None, silent=True):
        insert_query = """INSERT INTO keys (title, key)
                            VALUES (:key_title ,:key_pass)"""
        if title == "None":
            title = input("Title: ")
        if silent:
            salt, iv, enc = encrypt(
                getpass.getpass("Key: ").encode(), self.MasterPass.encode()
            )
            data = json.dumps({"salt": salt, "iv": iv, "enc": enc})
        else:
            salt, iv, enc = encrypt(
                input("Key: ").encode(), self.MasterPass.encode())
            data = json.dumps({"salt": salt, "iv": iv, "enc": enc})
        try:
            with opendb(self.db) as cur:
                cur.execute(insert_query, {
                            "key_title": title, "key_pass": data})
            print()
            print(f"[+]Stored Key for {title}")
        except sqlite3.Error as error:
            print("Failed to Insert Into Database", error)

    def noteins(self, title=None):
        insert_query = """INSERT INTO notes (title,content, date)
                            VALUES (:note_title ,:note_content, datetime())"""
        if title == "None":
            title = input("Title:")
        centext = "BODY"
        save_text = " Save [CTRL + D]  "
        discard = " Cancel [CTRL + C] "

        eq = (self.termlines // 2) - (len(save_text + centext + discard) // 2)
        last_put = " " * (eq) + centext + " " * (eq)
        print("_" * self.termlines)
        print(discard, end="")
        print(last_put, end="")
        print(save_text, end="")
        print("-" * self.termlines)

        note_content = "".join(sys.stdin.readlines())
        contb64 = base64.b64encode(note_content.encode())
        try:
            with opendb(self.db) as cur:
                cur.execute(
                    insert_query,
                    {
                        "note_title": title,
                        "note_content": contb64,
                    },
                )
            print()
            print(f"[+]Note Added")
        except sqlite3.Error as error:
            print("Failed to Insert Into Database", error)

    def remove_cd(self, table=None, u_id=None):
        query = f"DELETE FROM {table} WHERE id={u_id}"

        with opendb(self.db) as cur:
            cur.execute(query)

    def bigbang(self, boom=False, table_to_delete=None):
        if boom:
            clear_db()
        else:
            with opendb(self.db) as cur:
                cur.execute(f"DELETE FROM {table_to_delete}")

    def export(self, service=None, json=False, csv=False):
        backup = ""
        ext = ".json" if json else ".csv"
        if service == "passw":
            rawbac = self.view_userpasses(export=True)
            backup = rawbac.get_json_string() if json else rawbac.get_csv_string()

        elif service == "keys":
            rawbac = self.view_keys(export=True)
            backup = rawbac.get_json_string() if json else rawbac.get_csv_string()
        else:
            print("service name was not found")
        print(backup)
        with open("backup" + ext, "w") as f:
            for line in backup:
                if line != "\n":
                    f.write(line)
