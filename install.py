import os, getpass
import platform
from passwordManager.ciphers import finalhash 

# os.system("python -m pip install -r requirements.txt")
# os.system("python create_db.py")

linuxdir = os.path.expanduser("~/.local/share/pass.key")
windir = os.path.expanduser("~\\AppData\\pass.key")

def createpass(dir, txt):
    if not os.path.isfile(dir):
        with open(dir, 'wb') as f:
            f.write(txt)
            print("Passkey created")
    return "Already exist"
def setup():
    salt = 'xx01'
    while True:
        userInp = getpass.getpass("Create your Masterpass: ")
        userInp1 = getpass.getpass("Confirm Masterpass: ")
        if userInp == userInp1:
            keysalt = (userInp[-4:]+ salt) * 2
            # enc_mpass = encrypt(userInp.encode(), keysalt.encode())
            hashed_mpass = finalhash(userInp.encode(), keysalt.encode())
            if platform.system() == 'Linux':
                createpass(linuxdir, hashed_mpass.encode())
            else:
                createpass(windir, hashed_mpass.encode())
            break
if __name__ == "__main__":
    setup()
