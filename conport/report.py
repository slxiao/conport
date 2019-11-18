from jinja2 import Template
import datetime


def get_html_output(job_url, report_title, past_hours, summary, html5):
    # Get File Content in String
    jinja2_template_string = open("template.html", 'rb').read()

    # Create Template Object

    template = Template(jinja2_template_string)

    #summary = [{'case': u'Test Case Three', 'npass': 2, 'atoms': [(108, u'FAILED', 0.0), (109, u'FAILED', 0.0)], 'npass_numbers': [108, 109], 'pass': 0, 'fail_rate': 1.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 'NA'}, {'case': u'Test Case one', 'npass': 0, 'atoms': [(108, u'PASSED', 1.0), (109, u'PASSED', 1.0)], 'npass_numbers': [
    #    ], 'pass': 2, 'fail_rate': 0.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 1.0}, {'case': u'Test Case two', 'npass': 0, 'atoms': [(108, u'PASSED', 0.0), (109, u'PASSED', 1.0)], 'npass_numbers': [], 'pass': 2, 'fail_rate': 0.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 0.5}]

    config = {
    "past_hours": past_hours,
    "url": job_url,
    "title": report_title
    }

    for i in range(len(summary)):
        summary[i]["rank"] = i + 1

    build_trend = [
    {
        "number": 1,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 2,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 3,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 4,
        "pass": 1,
        "fail": 3
    },
    {
        "number": 5,
        "pass": 0,
        "fail": 4
    },
    {
        "number": 6,
        "pass": 0,
        "fail": 4
    },
    {
        "number": 7,
        "pass": 0,
        "fail": 4
    }
    ]

    # Render HTML Template String
    html_template_string = template.render(
        config=config, summary=summary, now=datetime.datetime.utcnow(), build_trend=build_trend, html5=True if html5 == "true" else False)
    return html_template_string
