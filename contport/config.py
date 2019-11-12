import configparser
import os

def parse_config_file(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config._sections

if __name__ == "__main__":
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "config.ini")
    print(parse_config_file(config_file))