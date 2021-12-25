import sys
from passwordManager import base
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




flags.add_argument("--ls","--showlist",action="store_const",help="Shows Credentials",const="all")
flags.add_argument("--rm","--remove",action="store_const",help="remove a credential",const="3")
flags.add_argument("--Ss","--search", metavar="" ,help="search trough credentials")
flags.add_argument("-T","--touch", action="store_true", help="Add new credential")

opt.add_argument("-U","--username",metavar="", help="Filter by Username")
opt.add_argument("-A" ,"--appname",metavar="",help="Filter by Appname")
opt.add_argument("-S" , "--sure" , action="store_true" ,help="Filter both we pass and username")
opt.add_argument("--c","--copy",action="store_true",help="Copy Pass to clip board")
opt.add_argument("--r",'--recent',action="store_true",help="Show recently modified credentials")
opt.add_argument("--w",'--warn',action="store_true",help="warn about weak passwords")


dan = parser.add_argument_group('Often Args :', '')

dan.add_argument("--bigbang",action="store_true",help="Erase all information")

                    


args = parser.parse_args()


USERNAME = args.username if args.username else None
APPNAME = args.appname if args.appname else None




if args.ls:
    if args.sure:
        db.viewdb_base(username=USERNAME,appname=APPNAME,state="and")

    elif args.appname or args.username:
        db.viewdb_base(username=USERNAME,appname=APPNAME)
    else:
        db.viewdb_base()


if args.touch:
    db.insert()


# if action == "help":
    # print(DASH)
# elif action == "add":
    # db.insert()
# elif action == "-a":
    # act_name = sys.argv[2]
    # print(act_name)
    # db.viewdb_by_appname(act_name)
# elif action == "-u":
    # act_name = sys.argv[2]
    # db.viewdb_by_username(act_name)

# elif action == "showall":
    # db.viewall()

# else:
    # print(action)
