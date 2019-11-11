from conport import figure


def test_get_binary_figure(mocker):
    mocked_plt = mocker.patch("conport.figure.plt")
    assert figure.get_binary_figure([
        {'fail': 1, 'number': 1, 'pass': 1}]) == ""
    mocked_plt.figure.assert_called()
