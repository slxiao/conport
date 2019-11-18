from conport.build import *


def test_get_jenkins_home():
    assert get_jenkins_home(
        "http://10.183.40.203:49001/job/test-robot-framework/") == "http://10.183.40.203:49001"
