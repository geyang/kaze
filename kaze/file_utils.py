import yaml


def load_yml(filename):
    try:
        with open(filename, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except FileNotFoundError:
        return None


def write_yml(data, filename):
    with open(filename, "w") as f:
        yaml.dump(data, f, sort_keys=False)
