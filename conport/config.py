import configparser
import os


class AttrDict(dict):
    def __init__(self, **response):
        for k, v in response.items():
            if isinstance(v, dict):
                self.__dict__[k] = AttrDict(**v)
            else:
                self.__dict__[k] = v


def parse_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return AttrDict(**config._sections)


def get_default_config():
    config_file = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "cfg.ini")
    return parse_config_file(config_file)
