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
