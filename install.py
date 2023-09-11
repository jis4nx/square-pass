import os
import getpass
import platform
from passwordManager.ciphers import finalhash

password_paths = {
    'Linux': os.path.expanduser("~/.local/share/pass.key"),
    'Windows': os.path.expanduser("~/AppData/pass.key")
}


def createpass(dir, txt):
    try:
        with open(dir, 'wb') as f:
            f.write(txt)
        print("Passkey created")
    except Exception as e:
        print(f"Failed to create passkey: {e}")


def setup():
    salt = 'xx01'
    while True:
        userInp = getpass.getpass("Create your Masterpass: ")
        userInp1 = getpass.getpass("Confirm Masterpass: ")
        if userInp == userInp1:
            keysalt = (userInp[-4:] + salt) * 2
            try:
                hashed_mpass = finalhash(userInp.encode(), keysalt.encode())
                os_name = platform.system()
                if os_name in password_paths:
                    createpass(password_paths[os_name], hashed_mpass.encode())
                else:
                    print("Unsupported OS")
            except ValueError:
                print('Choose a password between 4-32 characters long!')
            break


if __name__ == "__main__":
    setup()
