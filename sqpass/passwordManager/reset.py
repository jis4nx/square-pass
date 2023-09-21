from ciphers import decrypt, encrypt
import sqlite3

def resetpass():
    credlist = []
    conn = sqlite3.connect("../passwordmanager.db")
    cur = conn.cursor()
    mpass = """SELECT mspass from pass;"""
    keysalt = (mpass[-4:] + "xx01") * 2
    try:
        cur.execute(mpass)
        for x in cur.fetchall():
            credlist.append(x)
    except Exception as err:
        print(err)
    finally:
        if conn:
            conn.close()
    decpass = decrypt(mpass, keysalt)
    return decpass
print(resetpass())
