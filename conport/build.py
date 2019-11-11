import jenkins
import url

from datetime import datetime, timedelta
import time

ONE_HOUR_IN_MS = 1 * 60 * 60 * 1000


def get_boundary_timestamps(past_hours):
    end_timestamp = int(time.time() * 1000)
    start_timestamp = end_timestamp - int(past_hours) * ONE_HOUR_IN_MS
    return (start_timestamp, end_timestamp)


def build_in_boundary(past_hours, timestamp):
    start_timestamp, end_timestamp = get_boundary_timestamps(past_hours)
    return True if timestamp >= start_timestamp and timestamp < end_timestamp else False


def get_jenkins_home(job_url):
    myurl = url.parse(job_url)
    if myurl.port:
        return myurl.scheme + "://" + myurl.host + ":" + str(myurl.port)
    return myurl.scheme + "://" + myurl.host


def get_job_name(job_url):
    jenkins_home = get_jenkins_home(job_url)
    items = job_url.replace(jenkins_home, "").strip("/").split("job")
    return "/".join([i.strip("/") for i in items if i])


def get_jenkins_instance(job_url):
    jenkins_home = get_jenkins_home(job_url)
    return jenkins.Jenkins(jenkins_home)


def get_build_numbers(jenkins_instance, job_name):
    result = jenkins_instance.get_job_info(job_name)
    return [i["number"] for i in result["builds"]]


def get_test_reports(job_url, past_hours):
    test_reports = {}
    jenkins_instance = get_jenkins_instance(job_url)
    job_name = get_job_name(job_url)
    build_numbers = get_build_numbers(jenkins_instance, job_name)
    for number in build_numbers:
        build_info = jenkins_instance.get_build_info(job_name, number)
        if build_info["building"]:
            continue
        elif build_in_boundary(past_hours, build_info["timestamp"] + build_info["duration"]):
            report = jenkins_instance.get_build_test_report(job_name, number)
            test_reports[number] = {}
            test_reports[number]["duration"] = build_info["duration"]
            test_reports[number]["report"] = report
        else:
            break
    return test_reports
