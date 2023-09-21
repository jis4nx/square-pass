import os
import platform
import yaml


def get_config_path():
    os_name = platform.system()
    config_paths = {
        'Linux': os.path.expanduser("~/.config/sqpass/"),
        'Windows': os.path.expanduser("")
    }
    return config_paths.get(os_name, "")


def create_default_config():
    passw_colors = {
        "passw_colors": {
            'index': '',
            'username': '',
            'appname': '',
            'password': '',

        }
    }
    return yaml.dump(passw_colors, indent=4)


def setup_config():
    CONFIG_PATH = get_config_path()
    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
        path = os.path.join(CONFIG_PATH, "config.yaml")
        with open(path, "w") as f:
            f.write(create_default_config())
            print(f"Created config file at {path}")


def get_config():
    CONFIG_PATH = get_config_path()
    if os.path.exists(CONFIG_PATH):
        with open(os.path.join(CONFIG_PATH, "config.yaml"), "r") as f:
            data = yaml.load(f, Loader=yaml.SafeLoader)
            return data
