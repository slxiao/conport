from conport import report


def test_get_html_output(mocker):
    mocked_open = mocker.patch(
        "conport.report.open", mocker.mock_open(read_data=""))
    mocked_templated = mocker.patch("conport.report.Template")
    report.get_html_output("", "", "", "", "", "")
    mocked_open.assert_called()
    mocked_templated.assert_called()
