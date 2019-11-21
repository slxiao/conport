from __future__ import division
import datetime
import os
import sys

from jinja2 import Template


def get_template_path(report_lan):
    #TODO: merged chinese and english templates
    if report_lan == "english":
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "template.html")
    elif report_lan == "chinese":
        return os.path.join(os.path.abspath(os.path.dirname(__file__)), "template_cn.html")
    sys.exit("unsopprted report langure: %s" % report_lan)



def get_html_output(report_lan, job_url, report_title, past_hours, build_summary, case_summary, pure_html):
    jinja2_template_string = open(get_template_path(report_lan), 'r').read()
    template = Template(jinja2_template_string)

    build_metrics = {}
    build_metrics["avg_duration"] = round(sum(
        [i["duration"] for i in build_summary])/len(build_summary), 1) if len(build_summary) else "NA"
    passed_builds = [i["duration"] for i in build_summary if i["fail"] == 0]
    build_metrics["avg_duration_pass"] = "NA" if not passed_builds else round(sum(passed_builds
                                                                                  )/len(passed_builds), 1)
    build_metrics["max_duration"] = round(
        max([i["duration"] for i in build_summary]), 1) if [i["duration"] for i in build_summary] else "NA"
    build_metrics["max_pass_duration"] = round(max(
        passed_builds), 1) if passed_builds else "NA"

    html_template_string = template.render(build_metrics=build_metrics,
                                           job_url=job_url, report_title=report_title, past_hours=past_hours, case_summary=case_summary, now=datetime.datetime.utcnow(), build_summary=build_summary, pure_html=True if pure_html == "true" else False)

    return html_template_string
