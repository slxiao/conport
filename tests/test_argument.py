from conport import argument


def test_get_parser(mocker):
    mocker.patch("conport.argument.get_default_config",
                 return_value=mocker.Mock())
    mocked_parser = mocker.patch("argparse.ArgumentParser")
    argument.get_parser()
    mocked_parser.assert_called()
