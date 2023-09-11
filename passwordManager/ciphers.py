import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2


def encrypt(data, master_key):
    salt = get_random_bytes(16)
    key = PBKDF2(master_key, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))

    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    salt = base64.b64encode(salt).decode('utf-8')

    return salt, iv, ct


def decrypt(salt, iv, ct, master_key):
    salt = base64.b64decode(salt)
    iv = base64.b64decode(iv)[:16]
    ct = base64.b64decode(ct)
    key = PBKDF2(master_key, salt, dkLen=32)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decipher = unpad(cipher.decrypt(ct), AES.block_size)

    return decipher


def finalhash(msg, masterkey):
    masterkey = base64.b64encode(masterkey)
    IV = "agun".encode()*4
    cipher = AES.new(masterkey, AES.MODE_CFB, IV)
    encd = base64.b64encode(IV + cipher.encrypt(msg))
    return hashlib.sha256(encd).hexdigest()


def hashuser(masterkey):
    salt = 'xx01'
    keysalt = (masterkey[-4:] + salt) * 2
    try:
        hashed_mpass = finalhash(masterkey.encode(), keysalt.encode())
        return hashed_mpass
    except ValueError as e:
        print(e)
