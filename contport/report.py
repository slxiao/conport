from jinja2 import Template
import datetime


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

# Render HTML Template String
html_template_string = template.render(
    config=config, summary=summary, now=datetime.datetime.utcnow())


with open('output.html', 'w') as f:
    f.write(html_template_string)
