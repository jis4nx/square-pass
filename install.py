import os, getpass
import sqlite3
from passwordManager.ciphers import encrypt

# print("Installing Module....")
# os.system("pythom -m pip install -r requirements.txt")
# print("Creating Database....")
# os.system("python create_db.py")


ranbyte = os.urandom(16)
if not os.path.isfile("lol.enc"):
    while True:
        userInp = getpass.getpass("Create your Masterpass: ")
        userInp1 = getpass.getpass("Confirm Masterpass: ")
        if userInp == userInp1:
            try:
                conn = sqlite3.connect("passwordmanager.db")
                enc_mpass = encrypt(userInp.encode(), ranbyte)
            except Exception as err:
                print(err)
            break
    with open('pass.enc', 'wb') as f:
        f.write(enc_mpass)
else:
    pass



