import sys
from passwordManager import base
from passwordManager import argaction
import argparse

from colorama import Fore

green = Fore.GREEN
white = Fore.WHITE
red = Fore.RED



banner = f"""

      {green}   / / {red}(_)_ __  ___  ___  ___ _   _ _ __ ___  {white}            .
      {green}  / /  {red}| | '_ \/ __|/ _ \/ __| | | | '__/ _ \ {white}            .
    {green} _ / / {red}  | | | | \__ \  __/ (__| |_| | | |  __/{white}             .
    {green}(_)_/    {red}|_|_| |_|___/\___|\___|\__,_|_|  \___|{white}             .

""".center(2)




pwdwrong = ["Sorry that's not correct!",
            "Not even close!",
            "Nice Try!",
            "Hold on and give the correct password!"
            ]



#action = sys.argv[1]

db =base.DatabaseManager("shoaibislam")

parser = argparse.ArgumentParser(prog="ins",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=banner,
                                 epilog = "breh this will be the bottom line",
                                 conflict_handler="resolve",
                                 usage= "%(prog)s action [show|remove|search] "

                                 )

flags = parser.add_argument_group('Command :', '')
opt = parser.add_argument_group('Options :', '')




flags.add_argument("--ls","--showlist", nargs="?",            const="list", help="Shows Credentials")
flags.add_argument("--rm","--remove",   action="store_const",               help="remove a credential",const="3")
flags.add_argument("--Ss","--search",   action="store_true" , dest="search",help="search trough credentials")
flags.add_argument("--pp","--touchs",   action="store_true",                help="Add new credential")


opt.add_argument("-K",'--keypass',      metavar="",nargs="?", const="None", help="Add Key")
opt.add_argument("-N",'--note',         metavar="",nargs="?", const="None", help="Add Note")
opt.add_argument("-U","--username",     metavar="",                         help="Filter by Username")
opt.add_argument("-A" ,"--appname",     metavar="",                         help="Filter by Appname")
opt.add_argument("-S" , "--sure" ,      action="store_true" ,               help="Filter both we pass and username")
opt.add_argument("-C","--copy",         action="store_true",                help="Copy Pass to clip board")
opt.add_argument("-R",'--recent',       action="store_true",                help="Show recently modified credentials")
opt.add_argument("-W",'--warn',         action="store_true",                help="warn about weak passwords")
opt.add_argument("-i",'--index',        metavar="",           type=int,     help="Index for the credential update")
opt.add_argument("-d",'--update',   dest="update",nargs="?", const="None",  help="Update your credential service name")
opt.add_argument("-G", "--generate" ,  nargs="?" , type=int, const=8  ,     help="Generate Advance & Strong Pass")


dan = parser.add_argument_group('Often Args :', '')
dan.add_argument("--bigbang",metavar="",help="Erase all information")

                    


args = parser.parse_args()


USERNAME = args.username if args.username else None
APPNAME = args.appname if args.appname else None



def ls_list():
    print("All")
    print("Notes")
    print("UserPass")
    print("Keys")


if args.generate:
    passw = argaction.generate_password(args.generate)
    
    if args.copy:
        argaction.copy_to_clipboard(passw)

    print(passw)



if args.ls:
    sort = "date" if args.recent else "id"
    order = "DESC" if args.recent else "ASC"
    if args.recent:
        print("HELLO")
    if args.ls == "UserPass":
        db.view_userpasses(sort=sort, order=order)
    elif args.ls == "Notes":
        db.view_notes(sort=sort, order=order)
    elif args.ls == "Keys":
        db.view_keys(sort=sort, order=order)

    else:
        ls_list()


if args.search:
    if args.sure:
        db.viewdb_base(username=USERNAME,appname=APPNAME,state="and")

    elif args.appname or args.username:
        db.viewdb_base(username=USERNAME,appname=APPNAME)
    else:
        db.viewdb_base()


if args.keypass:
    if args.keypass == "None":
        db.keyins()
    else:
        db.keyins(args.keypass)

if args.pp:
    db.insert()

if args.note:
    if args.note == "None":
        db.noteins()
    else:
        db.noteins(args.note)


if args.bigbang:
    if args.bigbang == "boom":
        db.bigbang(boom=True)
    elif args.bigbang == "userpass":
        db.bigbang(userpass=True)
    elif args.bigbang == "keys":
        db.bigbang(keys=True)
    elif args.bigbang == "notes":
        db.bigbang(notes=True)
    else:
        pass

if args.update:
    if args.update == "None":
        print("Available arguements: \nusers | keys")
    else:
        if args.index:
            if args.update == "keys":
                db.update(table="keys", id=args.index)
            else:
                db.update(id=args.index)
        else:
            print("Please define an index number")



