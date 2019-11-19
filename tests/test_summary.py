from conport import summary

test_reports = {
    1: {
        "report": {
            "suites": [
                {
                    "name": "suite1",
                    "cases": [
                            {
                                "name": "case1",
                                "status": "PASSED",
                                "duration": 100
                            },
                        {
                                "name": "case2",
                                "status": "FAILED",
                                "duration": 100
                            }
                    ]
                }
            ]
        },
        "duration": 1
    }
}


def test_get_atom_reports():
    assert summary.get_atom_reports(test_reports) == [(
        1, 'suite1', 'case1', 'PASSED', 100), (1, 'suite1', 'case2', 'FAILED', 100)]


def test_get_merged_reports():
    atom_reports = [(
        1, 'suite1', 'case1', 'PASSED', 100), (1, 'suite1', 'case2', 'FAILED', 100)]
    assert summary.get_merged_reports(atom_reports) == {'suite1.case2': {'atoms': [
        (1, 'FAILED', 100)]}, 'suite1.case1': {'atoms': [(1, 'PASSED', 100)]}}


def test_get_case_summary():
    merged_reports = {'suite1.case2': {'atoms': [
        (1, 'FAILED', 100)]}, 'suite1.case1': {'atoms': [(1, 'PASSED', 100)]}}
    assert summary.get_ordered_reports(merged_reports).keys() == [
        'suite1.case2', 'suite1.case1']


def test_get_build_summary():
    assert summary.get_build_summary(test_reports) == [
        {'duration': 0.0, 'fail': 1, 'number': 1, 'pass': 1}]
