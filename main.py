import sys
import argparse
from passwordManager import base
from passwordManager import argaction
from passwordManager.ciphers import hashuser


pwdwrong = ["Sorry that's not correct!",
            "Not even close!",
            "Nice Try!",
            "Hold on and give the correct password!"
            ]




# userInp = input("Enter masterpass: ")
userInp = "shoaibislam"
db =base.DatabaseManager(userInp,hashuser(userInp))

parser = argparse.ArgumentParser(prog="ins",
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description="",
                                 epilog = "breh this will be the bottom line",
                                 conflict_handler="resolve",
                                 usage= "%(prog)s action [show|remove|search] "

                                 )

flags = parser.add_argument_group('Command :', '')
opt = parser.add_argument_group('Options :', '')




opt.add_argument("-U",'--update',       dest="update",metavar="",                           help="Update your credential with service name")
opt.add_argument("-cat",'--cat',        dest="cat",metavar="",                              help="View File")
opt.add_argument("-c",'--count',        dest="count",metavar="", nargs=2,                   help="Counts reused credential")
flags.add_argument("--ls","--showlist", dest="showlist",nargs="?",            const="list", help="Shows Credential")
flags.add_argument("--rm","--remove",   dest="remove",  metavar="",                         help="remove a credential")
flags.add_argument("-n","--normal",     dest="normal",action="store_true",                  help="Show key while typing")

#Insert
flags.add_argument("-P","--passw",      dest="passw",action="store_true",                   help="Add new credential")
opt.add_argument("-K",'--keypass',      dest="keypass",nargs="?", const="None",             help="Add Key")
opt.add_argument("-N",'--note',         dest="note",metavar="",nargs="?", const="None",     help="Add Note")

# Filter 
opt.add_argument("-u","--username",     dest="username",metavar="",                         help="Filter by Username")
opt.add_argument("-a" ,"--appname",     dest="appname",metavar="",                          help="Filter by Appname")
opt.add_argument("-b" , "--bp" ,        dest="user_pass",action="store_true" ,              help="Filter by both username and password")
opt.add_argument("-i",'--ignorecase',   dest="ignorecase",action="store_true",                       help="Index for the credential update")

# Opt args
opt.add_argument("-C","--copy",         dest="copy",action="store_true",                    help="Copy to clipboard")
opt.add_argument("-r",'--recent',       dest="recent",action="store_true",                  help="Show recently modified credentials")
# opt.add_argument("-W",'--warn',         action="store_true",                help="warn about weak passwords")

#Extra Args

dan = parser.add_argument_group('Often Args :', '')
dan.add_argument("--bigbang",           dest="bigbang",metavar="[boom | passw | keys | notes]",help="Erase Service information")
opt.add_argument("-g", "--gen" ,        dest="generate",nargs="?" , type=int, const=8  ,     help="Generate Advance & Strong Pass")
opt.add_argument("-e", "--export" ,        dest="export",nargs="+",     help="Generate Advance & Strong Pass")
                    


args = parser.parse_args()

services = ["passw", "notes", "keys"]

 
if args.passw:
    db.insert()

if args.keypass:
    mode = False if args.normal else True
    if args.keypass == "None":
        db.keyins(silent=mode)
    else:
        db.keyins(args.keypass, silent=mode)


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


if args.cat:
    try :
        idx = int(args.cat.split("/")[1])
        service = args.cat.split("/")[0]
        if service == "notes":
            db.view_notes(noteid=idx)
        elif service == "keys":
            db.view_keys(keyid=idx)
        elif service == "passw":
            db.view_userpasses(userid=idx)
        else:
            print("Availables: "," | ".join(services))
    except (IndexError, ValueError):
        print("Usage: sq -cat service/index")


if args.count:
    try:
        mode = True if args.ignorecase else False
        service = args.count[0].split("/")[0]
        field = args.count[0].split("/")[1]
        db.count(icase=mode,table=service, column=field, cred=args.count[1])
    except Exception as err:
        print(err)


if args.showlist:
    sort = "date" if args.recent else "id"
    order = "DESC" if args.recent else "ASC"
    mode = True if args.ignorecase else False
    if args.username:
        db.filter(icase=mode,username=args.username)
    elif args.appname:
        db.filter(icase=mode,appname=args.appname)
    else:
        if args.showlist == "passw":
            db.view_userpasses(sort=sort, order=order)
        elif args.showlist == "notes":
            db.view_notes(sort=sort, order=order)

        elif args.showlist == "keys":
            db.view_keys(sort=sort, order=order)

        else:
            print("Available Services:\n"+"_"*20)
            print("\n".join(services))


if args.remove:
    try:
        service_name = args.remove.split("/")[0]
        ind = int(args.remove.split("/")[1])
        try :
            db.remove_cd(table=service_name,u_id=ind)
        except KeyError:
            print("Available args:", " | ".join(services))
    except IndexError:
        print("Usage: sq --rm service/index")


if args.bigbang:
    if args.bigbang == "boom":
        db.bigbang(boom=True)

    elif args.bigbang == "passw":
        db.bigbang(userpass=True)
    elif args.bigbang == "keys":
        db.bigbang(keys=True)
    elif args.bigbang == "notes":
        db.bigbang(notes=True)
    else:
        print("Available args: \nboom | passw | keys | notes")



if args.update:
    service_name = args.update.split("/")[0] 
    ind = int(args.update.split("/")[1])
    try :
        db.update(table=service_name,id=ind)
    
    except KeyError:
        print("Availables: \nusers | keys")

if args.export:
    try:
        service_name = args.export[0]
        fileform = args.export[1]
    except IndexError:
        fileform = "json"
    if fileform == "csv":
        db.export(service=service_name,csv=True)
    elif fileform == "json":
        db.export(service=service_name,json=True)