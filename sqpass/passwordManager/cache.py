import time
import pickle
import os
import platform

cache_paths = {
    'Linux': os.path.expanduser("/tmp/"),
    'Windows': os.path.expanduser("")
}

os_name = platform.system()
CACHE_DIR = os.path.join(cache_paths.get(os_name, ""), "lvl.pk")

try:
    with open(CACHE_DIR, 'rb') as f:
        cache_data = pickle.load(f)
except FileNotFoundError:
    cache_data = {}


def save_cache_file():
    with open(CACHE_DIR, "wb") as f:
        pickle.dump(cache_data, f)


def set_with_ttl(key, value, ttl):
    exp_time = time.time() + (ttl * 60)
    cache_data[key] = (value, exp_time)
    save_cache_file()
