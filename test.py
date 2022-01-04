from passwordManager import base

db =base.DatabaseManager("shoaibislam")


print(db.count("passw", "username", "jis4nx"))
