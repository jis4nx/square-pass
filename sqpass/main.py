import os
import platform
from getpass import getpass
from sqpass.passwordManager import base
from sqpass.passwordManager import argaction
from sqpass.passwordManager.ciphers import hashuser, encrypt, decrypt
from sqpass.passwordManager.cache import get_valid_cache, set_with_ttl, CACHE_DIR
from sqpass.passwordManager.tools import is_process_running
from sqpass.passwordManager.parser import run_parser
from sqpass.passwordManager.base import readpass
from sqpass.install import password_path


from os import urandom

import subprocess

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
        if not os.path.exists(password_path):
            print("No Passkey found\nRun `sq-init` initialize")
            exit()
        get_cache_data = get_valid_cache()
        if get_cache_data:
            salt, iv, enc, rand_byte = get_cache_data
            upass = decrypt(salt, iv, enc, rand_byte).decode()
            self.userInp = upass
            self.db = base.DatabaseManager(
                self.userInp, hashuser(self.userInp))

            self.service_dict = {
                "passw": self.db.view_userpasses,
                "notes": self.db.view_notes,
                "keys": self.db.view_keys,
            }
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
            self.service_dict = {
                "passw": self.db.view_userpasses,
                "notes": self.db.view_notes,
                "keys": self.db.view_keys,
            }

    def show_usage(
        self,
        show_services=True,
        usage_msg=None,
        example=None,
        show_fields=False,
        arg=None,
    ):
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
            self.db.keyins(title=self.args.keypass, silent=mode)
        if note:
            self.db.noteins(title=self.args.note)

    def generate_password(self):
        passw = argaction.generate_password(self.args.generate)
        if self.args.copy:
            argaction.copy_to_clipboard(passw)
        print(passw)

    def handle_retrieve_data(self):
        try:
            idx = int(self.args.cat.split("/")[1])
            service = self.args.cat.split("/")[0]
            try:
                self.service_dict[service](indexId=idx)
            except KeyError:
                print("Availables: ", " | ".join(services))
        except (IndexError, ValueError):
            print("Usage: sq -cat service/index")

    def handle_count(self):
        try:
            mode = True if self.args.ignorecase else False
            service = self.args.count[0].split("/")[0]
            field = self.args.count[0].split("/")[1]
            self.db.count(
                icase=mode, table=service, column=field, cred=self.args.count[1]
            )
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
            try:
                self.service_dict[self.args.showlist](sort=sort, order=order)
            except KeyError:
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
        if self.args.bigbang in services:
            self.db.bigbang(table_to_delete=self.args.bigbang)
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
            salt, iv, enc = encrypt(self.userInp.encode("utf-8"), rand_byte)
            set_with_ttl("upass", [salt, iv, enc, rand_byte], int(cache_time))

            # path = os.path.join(
            #     os.path.dirname(os.path.abspath(__file__)), "observer.py"
            # )
            # if not is_process_running(path):
            #     if platform.system() == "Windows":
            #         subprocess.Popen(
            #             ["python", path], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            #     subprocess.Popen(["python", path])

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
            "count": self.handle_count,
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
