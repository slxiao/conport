
from __future__ import division
import collections


def get_atom_reports(test_reports):
    atom_reports = []
    for number, report in test_reports.iteritems():
        suites = report['report']['suites']
        for suite in suites:
            suite_name = suite['name']
            suite_cases = suite['cases']
            for suite_case in suite_cases:
                atom_reports.append(
                    (number, suite_name, suite_case['name'], suite_case['status'], suite_case['duration']))
    return atom_reports


def get_merged_reports(atom_reports):
    merged_reports = {}
    for atom in atom_reports:
        full_name = '.'.join([atom[1], atom[2]])
        if full_name not in merged_reports:
            merged_reports[full_name] = {
                'atoms': [(atom[0], atom[3], atom[4])]}
        else:
            merged_reports[full_name]['atoms'].append(
                (atom[0], atom[3], atom[4]))
    return merged_reports


def get_ordered_reports(merged_reports):
    for full_name, merged in merged_reports.iteritems():
        merged['pass'] = len([i for i in merged['atoms'] if i[1] == 'PASSED'])
        merged['npass'] = len([i for i in merged['atoms'] if i[1] != 'PASSED'])
        merged['fail_rate'] = merged['npass'] / len(merged['atoms'])
        merged['npass_numbers'] = [i[0]
                                   for i in merged['atoms'] if i[1] != 'PASSED']
        sum_pass_duration = sum([i[2]
                                 for i in merged['atoms'] if i[1] == 'PASSED'])
        merged['avg_pass_duration'] = sum_pass_duration / \
            merged['pass'] if merged['pass'] else "NA"

    print(merged_reports)
    sorted_merged_reports = sorted(
        merged_reports.items(), key=lambda x: x[1]['fail_rate'], reverse=True)

    return collections.OrderedDict(sorted_merged_reports)


def get_summary(test_reports):
    return get_ordered_reports(get_merged_reports(get_atom_reports(test_reports)))
