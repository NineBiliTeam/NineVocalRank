import yaml

config = {}


def init_config(path) -> dict:
    global config
    with open(path, "r", encoding="utf8") as f:
        config = yaml.safe_load(f)
    return config
