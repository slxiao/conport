from build import get_test_reports
from summary import get_summary


if __name__ == "__main__":
    # test_reports = get_test_reports(
    #    "http://10.183.40.203:49001/job/test-robot-framework/", "24")

    test_reports = {108: {'duration': 116631, 'report': {u'suites': [{u'enclosingBlocks': [], u'name': u'Robot-Framework-Bug', u'stdout': None, u'timestamp': None, u'nodeId': None, u'stderr': None, u'duration': 1.0, u'cases': [{u'status': u'PASSED', u'skipped': False, u'failedSince': 0, u'name': u'Test Case one', u'stdout': None, u'errorDetails': None, u'age': 0, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': None, u'skippedMessage': None, u'duration': 1.0, u'stderr': None}, {u'status': u'PASSED', u'skipped': False, u'failedSince': 0, u'name': u'Test Case two', u'stdout': None, u'errorDetails': None, u'age': 0, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': None, u'skippedMessage': None, u'duration': 0.0, u'stderr': None}, {u'status': u'FAILED', u'skipped': False, u'failedSince': 35, u'name': u'Test Case Three', u'stdout': None, u'errorDetails': u'1 != 2', u'age': 74, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': u'', u'skippedMessage': None, u'duration': 0.0, u'stderr': None}], u'enclosingBlockNames': [], u'id': None}], u'testActions': [], u'failCount': 1, u'skipCount': 0, u'duration': 1.0, u'passCount': 2, u'_class': u'hudson.tasks.junit.TestResult', u'empty': False}}, 109: {
        'duration': 4687, 'report': {u'suites': [{u'enclosingBlocks': [], u'name': u'Robot-Framework-Bug', u'stdout': None, u'timestamp': None, u'nodeId': None, u'stderr': None, u'duration': 2.0, u'cases': [{u'status': u'PASSED', u'skipped': False, u'failedSince': 0, u'name': u'Test Case one', u'stdout': None, u'errorDetails': None, u'age': 0, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': None, u'skippedMessage': None, u'duration': 1.0, u'stderr': None}, {u'status': u'PASSED', u'skipped': False, u'failedSince': 0, u'name': u'Test Case two', u'stdout': None, u'errorDetails': None, u'age': 0, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': None, u'skippedMessage': None, u'duration': 1.0, u'stderr': None}, {u'status': u'FAILED', u'skipped': False, u'failedSince': 35, u'name': u'Test Case Three', u'stdout': None, u'errorDetails': u'1 != 2', u'age': 75, u'testActions': [], u'className': u'Robot-Framework-Bug.TEST', u'errorStackTrace': u'', u'skippedMessage': None, u'duration': 0.0, u'stderr': None}], u'enclosingBlockNames': [], u'id': None}], u'testActions': [], u'failCount': 1, u'skipCount': 0, u'duration': 2.0, u'passCount': 2, u'_class': u'hudson.tasks.junit.TestResult', u'empty': False}}}

    print(get_summary(test_reports))