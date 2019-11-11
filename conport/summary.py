
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
        merged['suite'] = full_name.split('.')[0]
        merged['case'] = full_name.split('.')[1]
        merged['pass'] = len([i for i in merged['atoms'] if i[1] == 'PASSED'])
        merged['total'] = len(merged['atoms'])
        merged['npass'] = merged['total'] - merged['pass']
        merged['fail_rate'] = merged['npass'] / merged['total']
        merged['npass_numbers'] = [i[0]
                                   for i in merged['atoms'] if i[1] != 'PASSED']
        sum_pass_duration = sum([i[2]
                                 for i in merged['atoms'] if i[1] == 'PASSED'])
        merged['avg_pass_duration'] = round(
            sum_pass_duration / 1000 / merged['pass'], 1) if merged['pass'] else "NA"
        sum_duration = sum([i[2] for i in merged['atoms']])
        merged['avg_duration'] = round(sum_duration/1000 / merged['total'], 1)
        merged['max_duration'] = round(
            max([i[2]/1000 for i in merged['atoms']]), 1)
        merged['max_pass_duration'] = round(max([i[2]/1000
                                                 for i in merged['atoms'] if i[1] == 'PASSED']), 1) if merged['pass'] else "NA"

    sorted_merged_reports = sorted(
        merged_reports.items(), key=lambda x: (-1*x[1]['fail_rate'], x[1]["suite"], x[1]["case"]))

    return collections.OrderedDict(sorted_merged_reports)


def get_build_summary(test_reports):
    build_summary = []
    for number, report in test_reports.iteritems():
        build = {"number": number, "pass": 0,
                 "fail": 0, "duration": round(report["duration"]/1000, 1)}
        suites = report['report']['suites']
        for suite in suites:
            for case in suite['cases']:
                if case["status"] == "PASSED":
                    build["pass"] += 1
                else:
                    build["fail"] += 1
        build_summary.append(build)
    sorted(build_summary, key=lambda x: x["number"])
    return build_summary


def get_case_summary(test_reports):
    case_summary = get_ordered_reports(
        get_merged_reports(get_atom_reports(test_reports))).values()
    for i in range(len(case_summary)):
        case_summary[i]["rank"] = i + 1
    return case_summary
