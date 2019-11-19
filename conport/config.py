import configparser
import os
from attrdict import AttrDict


def parse_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return AttrDict(dict(config._sections))


def get_default_config():
    config_file = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "cfg.ini")
    return parse_config_file(config_file)
