import mock

from conport import build


@mock.patch("time.time", mock.Mock(return_value=1574066950))
def test_get_boundary_timestamps():
    assert build.get_boundary_timestamps(0) == (1574066950000, 1574066950000)
    assert build.get_boundary_timestamps(24) == (1573980550000, 1574066950000)


@mock.patch("conport.build.get_boundary_timestamps", mock.Mock(return_value=(0, 2)))
def test_build_in_boundary():
    assert build.build_in_boundary(24, 2) is False
    build.get_boundary_timestamps.assert_called_once_with(24)
    assert build.build_in_boundary(24, 1) is True
    assert build.build_in_boundary(24, 0) is True


def test_get_jenkins_home():
    assert build.get_jenkins_home(
        "http://127.0.0.1:8080/job/test-robot-framework/") == "http://127.0.0.1:8080"
    assert build.get_jenkins_home(
        "http://127.0.0.1/job/test-robot-framework/") == "http://127.0.0.1"


def test_get_job_name():
    assert build.get_job_name(
        "http://127.0.0.1:8080/job/test-robot-framework/") == "test-robot-framework"
    assert build.get_job_name(
        "http://127.0.0.1:8080/job/folder/job/test-robot-framework/") == "folder/test-robot-framework"


def test_get_jenkins_instance(mocker):
    mocked_get = mocker.patch(
        "conport.build.get_jenkins_home", mock.Mock(return_value="url"))
    mocked_jenkins = mocker.patch("jenkins.Jenkins")
    build.get_jenkins_instance("url")
    mocked_get.assert_called_once_with("url")
    mocked_jenkins.assert_called_once()


def test_get_build_numbers(mocker):
    mocked_jenkins_instance = mocker.Mock()
    mocked_jenkins_instance.get_job_info.return_value = {
        "builds": []}
    assert build.get_build_numbers(mocked_jenkins_instance, "job") == []
    mocked_jenkins_instance.get_job_info.assert_called_once_with("job")


def test_get_test_reports(mocker):
    mocked_jenkins_instance = mocker.Mock()
    mocker.patch(
        "conport.build.get_jenkins_instance", return_value=mocked_jenkins_instance)
    mocker.patch("conport.build.get_job_name")
    mocker.patch("conport.build.get_build_numbers")
    assert build.get_test_reports("url", 24) == {}

    mocker.patch("conport.build.get_build_numbers", return_value=[1, 2])
    mocked_jenkins_instance.get_build_info.return_value = {
        "building": True
    }
    assert build.get_test_reports("url", 24) == {}

    mocked_jenkins_instance.get_build_info.return_value = {
        "building": False,
        "timestamp": 1,
        "duration": 1
    }
    mocker.patch("conport.build.build_in_boundary", return_value=False)
    assert build.get_test_reports("url", 24) == {}

    mocker.patch("conport.build.build_in_boundary", return_value=True)
    mocked_jenkins_instance.get_build_test_report.return_value = {}
    assert build.get_test_reports("url", 24) == {
        1: {'duration': 1, 'report': {}}, 2: {'duration': 1, 'report': {}}}
