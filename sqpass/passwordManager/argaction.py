import pyperclip
import string
import random


def generate_password(passlen, lc=50, nc=30, pc=20):
    letters = list(string.ascii_letters)
    puncs = ['$', '#', '_', '-', '!', '@',
             '+', '&', '(', ')', '?', '.', '*', '%']
    digits = list(string.digits)

    def percent(char, pers):
        return int(pers*(char/100))

    password = ""
    password += "".join(random.choices(letters, k=percent(passlen, lc)))
    password += "".join(random.choices(puncs, k=percent(passlen, pc)))
    password += "".join(random.choices(digits, k=percent(passlen, nc)))

    breh = list(password)
    random.shuffle(breh)

    return "".join(breh)


def copy_to_clipboard(*argv, combo=False, divider=":"):
    """

    simply copy a string to clipboard or mixes gmail,password separated by `devider` 
    to make a combo and copy the full text into clipboard

    `*argv` : List of arguments

    `combo` ( options are either False or True ):
        False : Copies the first argument only .
        True : Copies the combo of all `argv` separated by `devider`

    `devider` : devides different argument

    e.g  : copy_to_clipboard( "This_is_A_pass" )

           copy_to_clipboard(

                        "helloworld@gmail.com",
                        "This_is_A_pass", 
                        combo=True , 
                        divider="-" 

                        )
    """

    if combo is False:
        pyperclip.copy(argv[0])
    else:
        combined_text = ""
        for arg in argv:
            if arg != argv[-1]:
                combined_text += str(arg)+divider
            else:
                combined_text += str(arg)

        pyperclip.copy(combined_text)


def show_hints(text, text_type="password", security=3, jokes=False):
    """
    text_types are :
        password
        gmail

    `security` : number of last digits to show as hint
    `jokes` : special feature for hint option . shows funny hints .

    """
    if jokes is False:
        amount_of_chars = len(text) - security + 1
        hidden_chars = "*" * amount_of_chars
        hint = text[0]+hidden_chars+text[-(security):]

        return (hint)

    else:
        pass
        # developments going on ( shoaib islam )
