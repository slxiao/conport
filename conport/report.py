from jinja2 import Template
import datetime


def get_html_output(html5):
    # Get File Content in String
    jinja2_template_string = open("template.html", 'rb').read()

    # Create Template Object
    print(jinja2_template_string)

    template = Template(jinja2_template_string)

    summary = [{'case': u'Test Case Three', 'npass': 2, 'atoms': [(108, u'FAILED', 0.0), (109, u'FAILED', 0.0)], 'npass_numbers': [108, 109], 'pass': 0, 'fail_rate': 1.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 'NA'}, {'case': u'Test Case one', 'npass': 0, 'atoms': [(108, u'PASSED', 1.0), (109, u'PASSED', 1.0)], 'npass_numbers': [
        ], 'pass': 2, 'fail_rate': 0.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 1.0}, {'case': u'Test Case two', 'npass': 0, 'atoms': [(108, u'PASSED', 0.0), (109, u'PASSED', 1.0)], 'npass_numbers': [], 'pass': 2, 'fail_rate': 0.0, 'suite': u'Robot-Framework-Bug', 'total': 2, 'avg_pass_duration': 0.5}]

    config = {
    "past_hours": 24,
    "url": 'http://mzoamci.eecloud.dynamic.nsn-net.net:8080/job/OAM_5GHZ_EIT_Regression/job/5g.classicbts.master.oam.EIT-regression/',
    "title": 'Here is 5G Classical BTS OAM Regression Testing Report(Master):'
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
        config=config, summary=summary, now=datetime.datetime.utcnow(), build_trend=build_trend, html5=html5)
    return html_template_string
