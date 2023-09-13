import argparse
from getpass import getpass
from passwordManager import base
from passwordManager import argaction
from passwordManager.ciphers import hashuser, encrypt, decrypt
from passwordManager.cache import set_with_ttl, CACHE_DIR
from os import urandom
from passwordManager.base import readpass
from subprocess import Popen
from passwordManager.tools import is_process_running
import pickle

pwdwrong = [
    "Sorry that's not correct!",
    "Not even close!",
    "Nice Try!",
    "Hold on and give the correct password!",
]


parser = argparse.ArgumentParser(
    prog="ins",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description="",
    epilog="Read Docs at https://github.com/jis4nx/square-pass",
    conflict_handler="resolve",
    usage="%(prog)s action [show|remove|search] ",
)

flags = parser.add_argument_group("Command :", "")
opt = parser.add_argument_group("Options :", "")


opt.add_argument(
    "-U",
    "--update",
    dest="update",
    metavar="",
    help="Update your credential with service name",
)
opt.add_argument(
    "-l", "--login", dest="login", metavar="", nargs="?", const="None", help="Login to remember password"
)
opt.add_argument("-cat", "--cat", dest="cat", metavar="", help="View File")
opt.add_argument(
    "-c", "--count", dest="count", metavar="", nargs=2, help="Counts reused credential"
)
flags.add_argument(
    "--ls",
    "--showlist",
    dest="showlist",
    nargs="?",
    const="list",
    help="Shows Credential",
)
flags.add_argument(
    "--rm", "--remove", dest="remove", metavar="", help="remove a credential"
)
flags.add_argument(
    "-n", "--normal", dest="normal", action="store_true", help="Show key while typing"
)

# Insert
flags.add_argument(
    "-P", "--passw", dest="passw", action="store_true", help="Add new credential"
)
opt.add_argument(
    "-K", "--keypass", dest="keypass", nargs="?", const="None", help="Add Key"
)
opt.add_argument(
    "-N", "--note", dest="note", metavar="", nargs="?", const="None", help="Add Note"
)

# Filter
opt.add_argument(
    "-u", "--username", dest="username", metavar="", help="Filter by Username"
)
opt.add_argument(
    "-a", "--appname", dest="appname", metavar="", help="Filter by Appname"
)
opt.add_argument(
    "-b",
    "--bp",
    dest="user_pass",
    action="store_true",
    help="Filter by both username and password",
)
opt.add_argument(
    "-i",
    "--ignorecase",
    dest="ignorecase",
    action="store_true",
    help="Index for the credential update",
)

# Opt args
opt.add_argument(
    "-C", "--copy", dest="copy", action="store_true", help="Copy to clipboard"
)
opt.add_argument(
    "-r",
    "--recent",
    dest="recent",
    action="store_true",
    help="Show recently modified credentials",
)
# opt.add_argument("-W",'--warn',         action="store_true",                help="warn about weak passwords")

# Extra Args

dan = parser.add_argument_group("Often Args :", "")
dan.add_argument(
    "--bigbang",
    dest="bigbang",
    metavar="[boom | passw | keys | notes]",
    help="Erase Service information",
)
opt.add_argument(
    "-g",
    "--gen",
    dest="generate",
    nargs="?",
    type=int,
    const=8,
    help="Generate Advance & Strong Pass",
)
opt.add_argument(
    "-e", "--export", dest="export", nargs="+", help="Generate Advance & Strong Pass"
)


args = parser.parse_args()

services = ["passw", "notes", "keys"]


class UserArgManager:
    def __init__(self):
        self.userInp = None
        self.db = None

    def setup(self):
        try:
            with open(CACHE_DIR, 'rb') as f:
                data = pickle.load(f)
        except FileNotFoundError:
            data = None
            with open(CACHE_DIR, 'wb') as f:
                pickle.dump(data, f)

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
            mode = False if args.normal else True
            if args.keypass == "None":
                self.db.keyins(silent=mode)
            else:
                self.db.keyins(args.keypass, silent=mode)
        if note:
            if note == "None":
                self.db.noteins()
            else:
                self.db.noteins(args.note)

    def generate_password(self):
        passw = argaction.generate_password(args.generate)
        if args.copy:
            argaction.copy_to_clipboard(passw)
        print(passw)

    def handle_retrieve_data(self):
        try:
            idx = int(args.cat.split("/")[1])
            service = args.cat.split("/")[0]
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
            mode = True if args.ignorecase else False
            service = args.count[0].split("/")[0]
            field = args.count[0].split("/")[1]
            self.db.count(icase=mode, table=service,
                          column=field, cred=args.count[1])
        except Exception as err:
            print(err)

    def handle_showlist(self):
        sort = "date" if args.recent else "id"
        order = "DESC" if args.recent else "ASC"
        mode = True if args.ignorecase else False
        if args.username:
            self.db.filter(icase=mode, username=args.username)
        elif args.appname:
            self.db.filter(icase=mode, appname=args.appname)
        else:
            if args.showlist == "passw":
                self.db.view_userpasses(sort=sort, order=order)
            elif args.showlist == "notes":
                self.db.view_notes(sort=sort, order=order)

            elif args.showlist == "keys":
                self.db.view_keys(sort=sort, order=order)

            else:
                self.show_usage(arg="--ls", example="passw",
                                usage_msg="<service>")

    def handle_remove(self):
        try:
            service_name = args.remove.split("/")[0]
            ind = int(args.remove.split("/")[1])
            try:
                self.db.remove_cd(table=service_name, u_id=ind)
            except KeyError:
                print("Available args:", " | ".join(services))
        except IndexError:
            print("Usage: sq --rm service/index")

    def handle_bigbang(self):
        if args.bigbang == "boom":
            self.db.bigbang(boom=True)

        elif args.bigbang == "passw":
            self.db.bigbang(userpass=True)
        elif args.bigbang == "keys":
            self.db.bigbang(keys=True)
        elif args.bigbang == "notes":
            self.db.bigbang(notes=True)
        else:
            print("Available args: \nboom | passw | keys | notes")

    def handle_update(self):
        usage = r"sq -U <service>/<index>"
        eg = "sq -U passw/2"
        try:
            service_name = args.update.split("/")[0]
            index = int(args.update.split("/")[1])
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
            service_name = args.export[0]
            fileform = args.export[1]
        except IndexError:
            fileform = "json"
        if fileform == "csv":
            self.db.export(service=service_name, csv=True)
        elif fileform == "json":
            self.db.export(service=service_name, json=True)

    def handle_login(self):
        if args.login:
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

    def handle_functions(self):
        actions = {
            "update": self.handle_update,
            "export": self.handle_export,
            "bigbang": self.handle_bigbang,
            "remove": self.handle_remove,
            "showlist": self.handle_showlist,
            "cat": self.handle_retrieve_data,
            "note": lambda: self.handle_insert(note=args.note),
            "passw": lambda: self.handle_insert(passw=True),
            "keypass": lambda: self.handle_insert(keypass=True),
            "generate": self.generate_password,
            "login": self.handle_login
        }

        for arg, action in actions.items():
            if getattr(args, arg):
                action()


if __name__ == "__main__":
    argmanager = UserArgManager()
    argmanager.setup()
    argmanager.handle_functions()
