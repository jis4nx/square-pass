import pickle
import time
import os

CACHE_FILE = "/tmp/lvl.pk"

while True:
    if os.path.exists(CACHE_FILE) and os.path.getsize(CACHE_FILE) > 0:
        try:
            with open(CACHE_FILE, 'rb') as file:
                cache = pickle.load(file)
                try:
                    if 'upass' in cache:
                        value, exp_time = cache['upass']
                        if exp_time < time.time():
                            with open(CACHE_FILE, 'wb') as clear_file:
                                pickle.dump({}, clear_file)
                except ValueError:
                    pass
        except (FileNotFoundError, EOFError, pickle.UnpicklingError):
            pass

    time.sleep(1)
