import datetime
import os

from jinja2 import Template


def get_template_path():
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "template.html")


def get_html_output(job_url, report_title, past_hours, build_summary, case_summary, pure_html):
    jinja2_template_string = open(get_template_path(), 'rb').read()
    template = Template(jinja2_template_string)

    html_template_string = template.render(
        job_url=job_url, report_title=report_title, past_hours=past_hours, case_summary=case_summary, now=datetime.datetime.utcnow(), build_summary=build_summary, pure_html=True if pure_html == "true" else False)

    return html_template_string
