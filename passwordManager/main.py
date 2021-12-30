import sys
import time
t0 = time.time()
from passwordManager import base
from passwordManager import argaction
import argparse

from colorama import Fore
t1 = time.time()
print(t1-t0)

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
flags.add_argument("--rm","--remove", dest="remove",  nargs="?",            const="list", help="remove a credential")
flags.add_argument("--s","--silent",   action="store_true",help="search trough credentials")
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
opt.add_argument("-lsf",'--filedex',      metavar="", help="View File")

dan = parser.add_argument_group('Often Args :', '')
dan.add_argument("--bigbang",metavar="",help="Erase all information")

                    


argso = parser.parse_args()



def main(args=argso):
    def ls_list():
        print("All")
        print("Notes")
        print("UserPass")
        print("Keys")


     
    if args.pp:
        db.insert()

    if args.keypass:
        if args.keypass == "None":
            db.keyins()
        else:
            db.keyins(args.keypass)

    if args.note:

        if args.note == "None":
            db.noteins()
        else:
            db.noteins(args.note)





    if args.generate:
        passw = argaction.generate_password(args.generate)
        
        if args.copy:
            argaction.copy_to_clipboard(passw)

        print(passw)


    if args.ls:
        sort = "date" if args.recent else "id"
        order = "DESC" if args.recent else "ASC"
        indexarg = args.index if args.index else None
        username = args.username if args.username else None
        appname = args.appname if args.appname else None
        
        services = {
                    "UserPass":db.viewdb_base(username=username,appname=appname,state="or"),
                    "Notes":db.view_notes(sort=sort, order=order,noteid=indexarg),
                    "Keys": db.view_keys(sort=sort, order=order)
        }

        try:
            services[args.ls]
        except:
            ls_list()



    if args.remove:
        if not args.index and not args.findex:
            print("Must have One Index")

        else:

            service_names = ["users","keys"]
            service_name = args.findex.split("/")[0] if args.findex else args.update
            ind = int(args.findex.split("/")[1]) if args.findex else args.index
            try :
                db.remove_cd(table=service_name,u_id=ind)
            except KeyError:
                print("Available arguements: \nusers | keys | notes")




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
        if not args.index and not args.findex:
            print("Must have One Index")

        else:

            service_names = ["users","keys"]
            service_name = args.findex.split("/")[0] if args.findex else args.update
            ind = int(args.findex.split("/")[1]) if args.findex else args.index

            try :

                db.update(table=service_name,id=ind)
            
            except KeyError:
                print("Availables: \nusers | keys")


if __name__ == "__main__":
    pass
