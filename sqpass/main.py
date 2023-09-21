import os
from getpass import getpass
from sqpass.passwordManager import base
from sqpass.passwordManager import argaction
from sqpass.passwordManager.ciphers import hashuser, encrypt, decrypt
from sqpass.passwordManager.cache import set_with_ttl, CACHE_DIR
from sqpass.passwordManager.tools import is_process_running
from sqpass.passwordManager.parser import run_parser
from sqpass.passwordManager.base import readpass, pathname


from os import urandom

from subprocess import Popen

import pickle

pwdwrong = [
    "Sorry that's not correct!",
    "Not even close!",
    "Nice Try!",
    "Hold on and give the correct password!",
]

services = ["passw", "notes", "keys"]


class UserArgManager:
    def __init__(self, args):
        self.userInp = None
        self.db = None
        self.args = args

    def setup(self):
        data = None
        if os.path.exists(CACHE_DIR):
            with open(CACHE_DIR, 'rb') as file:
                data = pickle.load(file)

        if not os.path.exists(pathname):
            print('No Passkey found\nRun `sq-init` initialize')
            exit()
        if data:
            salt, iv, enc, rand_byte = data['upass'][0]
            upass = decrypt(salt, iv, enc, rand_byte).decode()
            self.userInp = upass
            self.db = base.DatabaseManager(
                self.userInp, hashuser(self.userInp))
        else:
            userpass = getpass(prompt="Enter Masterpass: ")
            hashed_pass = hashuser(userpass)
            while True:
                if hashed_pass != readpass():
                    userpass = getpass(prompt="Try again: ")
                    hashed_pass = hashuser(userpass)
                else:
                    self.userInp = userpass
                    break
            self.db = base.DatabaseManager(
                self.userInp, hashuser(self.userInp))

    def show_usage(self, show_services=True, usage_msg=None, example=None, show_fields=False, arg=None):
        print("")
        if show_services:
            print(f"Available Services -[ {' | '.join(services)} ]")
        if usage_msg is not None:
            print(f"usage: sq {arg} {usage_msg}")
        if example is not None:
            print(f"eg: sq {arg} {example}")
        if show_fields:
            pass
        print("")

    def handle_insert(self, passw=False, keypass=False, note=False):
        if passw:
            self.db.insert()
        if keypass:
            mode = False if self.args.normal else True
            if self.args.keypass == "None":
                self.db.keyins(silent=mode)
            else:
                self.db.keyins(self.args.keypass, silent=mode)
        if note:
            if note == "None":
                self.db.noteins()
            else:
                self.db.noteins(self.args.note)

    def generate_password(self):
        passw = argaction.generate_password(self.args.generate)
        if self.args.copy:
            argaction.copy_to_clipboard(passw)
        print(passw)

    def handle_retrieve_data(self):
        try:
            idx = int(self.args.cat.split("/")[1])
            service = self.args.cat.split("/")[0]
            if service == "notes":
                self.db.view_notes(noteid=idx)
            elif service == "keys":
                self.db.view_keys(keyid=idx)
            elif service == "passw":
                self.db.view_userpasses(userid=idx)
            else:
                print("Availables: ", " | ".join(services))
        except (IndexError, ValueError):
            print("Usage: sq -cat service/index")

    def handle_count(self):
        try:
            mode = True if self.args.ignorecase else False
            service = self.args.count[0].split("/")[0]
            field = self.args.count[0].split("/")[1]
            self.db.count(icase=mode, table=service,
                          column=field, cred=self.args.count[1])
        except Exception as err:
            print(err)

    def handle_showlist(self):
        sort = "date" if self.args.recent else "id"
        order = "DESC" if self.args.recent else "ASC"
        mode = True if self.args.ignorecase else False
        if self.args.username:
            self.db.filter(icase=mode, username=self.args.username)
        elif self.args.appname:
            self.db.filter(icase=mode, appname=self.args.appname)
        else:
            if self.args.showlist == "passw":
                self.db.view_userpasses(sort=sort, order=order)
            elif self.args.showlist == "notes":
                self.db.view_notes(sort=sort, order=order)

            elif self.args.showlist == "keys":
                self.db.view_keys(sort=sort, order=order)

            else:
                self.show_usage(arg="--ls", example="passw",
                                usage_msg="<service>")

    def handle_remove(self):
        try:
            service_name = self.args.remove.split("/")[0]
            ind = int(self.args.remove.split("/")[1])
            try:
                self.db.remove_cd(table=service_name, u_id=ind)
            except KeyError:
                print("Available args:", " | ".join(services))
        except IndexError:
            print("Usage: sq --rm service/index")

    def handle_bigbang(self):
        if self.args.bigbang == "boom":
            self.db.bigbang(boom=True)

        elif self.args.bigbang == "passw":
            self.db.bigbang(userpass=True)
        elif self.args.bigbang == "keys":
            self.db.bigbang(keys=True)
        elif self.args.bigbang == "notes":
            self.db.bigbang(notes=True)
        else:
            print("Available args: \nboom | passw | keys | notes")

    def handle_update(self):
        usage = r"sq -U <service>/<index>"
        eg = "sq -U passw/2"
        try:
            service_name = self.args.update.split("/")[0]
            index = int(self.args.update.split("/")[1])
            if service_name not in services:
                self.show_usage(show_services=True,
                                usage_msg=usage, example=eg)
                return
            try:
                self.db.update(table=service_name, id=index)
            except Exception as e:
                print(e)
                print("Availables: \nusers | keys")

        except Exception as e:
            self.show_usage(show_services=True, usage_msg=usage, example=eg)

    def handle_export(self):
        try:
            service_name = self.args.export[0]
            fileform = self.args.export[1]
        except IndexError:
            fileform = "json"
        if fileform == "csv":
            self.db.export(service=service_name, csv=True)
        elif fileform == "json":
            self.db.export(service=service_name, json=True)

    def handle_login(self):
        if self.args.login:
            cache_time = input("Time duration to remember <minutes> : ")
            while True:
                if not cache_time.isdigit():
                    cache_time = input("Please Enter minutes in number: ")
                else:
                    break
            rand_byte = urandom(16)
            salt, iv, enc = encrypt(self.userInp.encode('utf-8'), rand_byte)
            set_with_ttl('upass', [salt, iv, enc, rand_byte], int(cache_time))
            cmd = ['python', 'observer.py']
            if not is_process_running(cmd):
                Popen(['python', 'observer.py'],
                      start_new_session=True)

    def initial_setup(self):
        pass

    def handle_functions(self):
        actions = {
            "update": self.handle_update,
            "export": self.handle_export,
            "bigbang": self.handle_bigbang,
            "remove": self.handle_remove,
            "showlist": self.handle_showlist,
            "cat": self.handle_retrieve_data,
            "note": lambda: self.handle_insert(note=self.args.note),
            "passw": lambda: self.handle_insert(passw=True),
            "keypass": lambda: self.handle_insert(keypass=True),
            "generate": self.generate_password,
            "login": self.handle_login,
        }

        for arg, action in actions.items():
            if getattr(self.args, arg):
                action()


def main():
    argmanager = UserArgManager(args=run_parser())
    argmanager.setup()
    argmanager.handle_functions()


if __name__ == "__main__":
    main()
