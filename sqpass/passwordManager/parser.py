import argparse


def run_parser():

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
    return args
