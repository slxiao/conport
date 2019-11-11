from conport import config


def test_AttrDict():
    d = {
        "a": {
            "b": 1
        }
    }
    assert config.AttrDict(**d).a.b == 1


def test_parse_config_file(mocker):
    mocked_parser = mocker.patch("configparser.ConfigParser")
    config.parse_config_file(mocker.Mock())
    assert mocked_parser.called


def test_get_default_config(mocker):
    mocked_parse = mocker.patch("conport.config.parse_config_file")
    config.get_default_config()
    mocked_parse.assert_called()
