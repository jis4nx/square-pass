import base64, hashlib
from Crypto.Cipher import AES 
import os

def encrypt(msg, masterkey):
    masterkey = base64.b64encode(masterkey) 
    IV = os.urandom(16)
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    return base64.b64encode(IV + cipher.encrypt(msg))

def decrypt(encMsg, masterkey):
    masterkey = base64.b64encode(masterkey) 
    encMsg = base64.b64decode(encMsg)
    IV = encMsg[:AES.block_size]
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    return cipher.decrypt(encMsg[AES.block_size:])

def finalhash(msg, masterkey):
    masterkey = base64.b64encode(masterkey) 
    IV = "agun".encode()*4
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    encd = base64.b64encode(IV + cipher.encrypt(msg))
    return hashlib.sha256(encd).hexdigest()


