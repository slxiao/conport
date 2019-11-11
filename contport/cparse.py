#!/usr/bin/python
"""
Purpose of the script:
    1. Parse the stress testing result
    2. Sent the stress testing report to relative team
Usage: python cparse.py branch [debug|to <to_list> {<cc_list>}|cc <cc_list>]
Example:
1. debug mode              : python cparse.py branch debug
2. set to list             : python cparse.py branch to 'chao.kuang@nokia-sbell.com, tao.1.fan@nokia-sbell.com'
3. set cc list             : python cparse.py branch cc 'chao.kuang@nokia-sbell.com, tao.1.fan@nokia-sbell.com'
4. set to list and cc list : python cparse.py branch to 'chao.kuang@nokia-sbell.com' 'tao.1.fan@nokia-sbell.com'
Note:
    * branch is SRAN17A_P7/SRAN17A_MP/SRAN18/TRUNK
    * to_list/cc_list need to separated by command and whitespace
"""

import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from gevent import monkey

monkey.patch_all()
import time
import requests
import itertools
import smtplib
from lxml import etree

from gevent.pool import Pool as Gpool
from multiprocessing import Process
from email.mime.text import MIMEText
from datetime import datetime, timedelta, date

TIME = ['00:00:00', '23:59:59']
FEATURE_GENERATOR = itertools.count(1)
REGRESSION_GENERATOR = itertools.count(1)
TIMEOUT_GENERATOR = itertools.count(1)
TIMEOUT_MESSAGE = ['fatal error', 'terminated by signal']
SUITE_PATTERN = re.compile(r'Test Suites.+?page_generated', re.S)
TEST_PATTERN = re.compile(r'Test Cases<.+?page_generated', re.S)
HREF_PATTERN = re.compile(r'<a href=.+?</a>', re.S)
TAGS_PATTERN = re.compile(r'<th>Tags:</th>.+?</td>', re.S)
RESULT_PATTERN = re.compile(r'<th>Status:</th>.+?</td>', re.S)
MESSAGE_PATTERN = re.compile(r'<th>Message:</th>.+?</td>', re.S)
SENDER = 'I_EXT_MBB_GLOBAL_LTE_TDD_OM_CI@internal.nsn.com'
DEFAULT_TO = ['I_MN_MANO_SOAM5_SPRING_GMS <I_MN_MANO_SOAM5_SPRING@internal.nsn.com>', 'jian-ken.zhang@nokia-sbell.com', 'caixia.pu@nokia-sbell.com']
DEFAULT_CC = ['I_EXT_MBB_GLOBAL_LTE_TDD_OM_CI@internal.nsn.com']


class SentEmail(object):
    def __init__(self, report, log):
        self._mail_host = 'mailrelay.int.nokia.com'
        self._mail_user = 'tdd_lte_oam_ci'
        self._mail_password = ''
        self._msg = None
        self._log = log
        self.report = report

    def run(self):
        self._generate_mail_text()
        self._sent_email()

    def _get_xml_content(self):
        with open(self._log, 'rb') as fp:
            content = fp.read()
        return content

    def _generate_mail_text(self):
        _msg = MIMEText('Hello\n\n%s\n%s' % (self._get_xml_content(), 'Best Regards'), 'html', 'utf-8')
        _msg['From'] = SENDER
        _msg['To'] = ';'.join(TO_RECEIVERS)
        _msg['Cc'] = ';'.join(CC_RECEIVERS)
        _msg['Subject'] = '[%s] %s' % (date.today(), self.report)
        self._msg = _msg

    def _sent_email(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self._mail_host, 25)
            try:
                smtpobj.login(self._mail_user, self._mail_password)
            except Exception:
                pass
            smtpobj.sendmail(self._msg['From'], (self._msg['To'] + ';' + self._msg['Cc']).split(';'),
                             self._msg.as_string())
            smtpobj.quit()
            print "[%s]INFO: Sent email successfully!" % get_timestamp()
        except smtplib.SMTPException as e:
            raise RuntimeError("[%s]ERROR: Can not send email. Error is %s." % (get_timestamp(), str(e)))


class Parse(Process):
    def __init__(self, name, stress_link, log, report, flag=True):
        Process.__init__(self)
        self.name = name
        self.stress_link = stress_link
        self.log = log
        self.report = report
        self.flag = flag
        self.feature = {}
        self.regression = {}
        self.timeout = {}
        self.time = []
        self.resource = []
        self.fail_list = []
        self.owner = []
        self.fail_list = []
        self.request = requests.Session()
        self.num = self._get_suiteable_num()

    def run(self):
        gpool = Gpool(4)
        gpool.map(self._get_resource_content, [num for num in self.num])
        for content in self.resource:
            self._get_all_cases(content)
        self._generate_html()
        if self.owner:
            self._at_failed_case_owner()
        if self.fail_list:
            self._at_ci_team()
        print '[%s]INFO: Generate html report successfully.' % get_timestamp()
        if self.flag:
            SentEmail(self.report, self.log).run()
        else:
            print '[%s]INFO: Not sent email for debug level.' % get_timestamp()

    def _get_resource_content(self, num):
        link = self.stress_link + str(num) + '/robot'
        r = self.request.get(link)
        if r.status_code in [200]:
            content = SUITE_PATTERN.search(r.content).group()
            for g in HREF_PATTERN.finditer(content):
                suite_name, suite_link = self._get_name_and_link(g.group(0), link)
                if suite_name:
                    suite_info = self._parse_suite_resource(suite_name, suite_link, num)
                    self.resource.append(suite_info)
        else:
            print '[%s]WARN: Link %s is invalid! error %s' % (get_timestamp(), link, r.status_code)
            self.fail_list.append(num)

    def _parse_suite_resource(self, name, link, num):
        suite_info = {'suite_name':name, 'test':[], 'num': num}
        r = self.request.get(link)
        if r.status_code in [200]:
            content = TEST_PATTERN.search(r.content).group()
            for g in HREF_PATTERN.finditer(content):
                test_name, test_link = self._get_name_and_link(g.group(0), link)
                test_info = self._parse_test_resource(test_name, test_link, num)
                suite_info['test'].append(test_info)
        else:
            print '[%s]WARN: Link %s is invalid! error %s' % (get_timestamp(), link, r.status_code)
            self.fail_list.append(num)
        return suite_info

    def _parse_test_resource(self, name, link, num):
        test_info = {'owner': '', 'status': '', 'result': '', 'test_name': '', 'timeout': ''}
        r = self.request.get(link)
        if r.status_code in [200]:
            tags = TAGS_PATTERN.search(r.content).group()
            owner = 'owner-' in tags and tags.split('owner-')[-1].split(',')[0] or 'unknow'
            status = 'status-' in tags and tags.split('status-')[-1].split(',')[0] or 'unknow'
            result = RESULT_PATTERN.search(r.content).group()
            result = result.split('">')[-1].split('</')[0]
            message = MESSAGE_PATTERN.search(r.content)
            if message and filter(lambda x: x in message.group(), TIMEOUT_MESSAGE):
                timeout = True
            else:
                timeout = False
            test_info.update({'owner': owner, 'status': status, 'result': result, 'test_name': name, 'timeout': timeout})
        else:
            print '[%s]WARN: Link %s is invalid! error %s' % (get_timestamp(), link, r.status_code)
            self.fail_list.append(num)
        return test_info

    def _get_name_and_link(self, content, link):
        if '</small>' in content:
            name = content.split('</small>')[-1].split('</a>')[0]
        else:
            name = content.split('">')[-1].split('</a>')[0]
        name = name.split(self.name)[-1].strip() and name or ''
        suffix = content.split('href="')[-1].split('">')[0]
        link = link + '/' + suffix.replace('amp;', '')
        return name, link

    def _get_all_cases(self, content):
        for test in content['test']:
            suite_name = content['suite_name']
            num = content['num']
            if test['status'] == 'RT':
                self._add_cases_to_container(test, self.regression, suite_name, num)
            elif test['status'] == 'done':
                self._add_cases_to_container(test, self.feature, suite_name, num)

    def _add_cases_to_container(self, test, container, suite, num):
        long_name = suite + '/' + test['test_name']
        if not test['timeout']:
            if long_name not in container:
                if test['result'] == 'PASS':
                    container[long_name] = {'total': 1, 'failed': [], 'owner': test['owner']}
                else:
                    container[long_name] = {'total': 1, 'failed': [num], 'owner': test['owner']}
            else:
                if test['result'] == 'PASS':
                    container[long_name]['total'] += 1
                else:
                    container[long_name]['total'] += 1
                    container[long_name]['failed'].append(num)
        else:
            if long_name not in self.timeout:
                self.timeout[long_name] = {'total': 1, 'failed': [num], 'owner': test['owner']}
            else:
                self.timeout[long_name]['total'] += 1
                self.timeout[long_name]['failed'].append(num)

    def _get_suiteable_num(self):
        start, end = self._get_suitable_timestamp()
        link = '%sapi/xml?tree=builds[number,result,timestamp]&exclude=//build[%s>timestamp or timestamp>%s]' % (
            self.stress_link, start, end)
        print '[%s]INFO: Parse the jenkins api for "%s"' % (get_timestamp(), link)
        xml = self.request.get(link).content
        root = etree.fromstring(xml)
        num = root.xpath('build/number/text()')
        if not num:
            raise RuntimeError("Can't find valid builds in stress testing job.")
        return num

    def _get_suitable_timestamp(self):
        bj_time = datetime.utcfromtimestamp(time.time()) + timedelta(hours=8)  # get current beijing time
        bj_yesterday = bj_time - timedelta(days=1)  # get yesterday time
        yesterday_start = str(bj_yesterday).split()[0] + ' %s' % TIME[0]
        yesterday_end = str(bj_yesterday).split()[0] + ' %s' % TIME[1]
        print '[%s]INFO: yesterday is start %s and end %s' % (get_timestamp(), yesterday_start, yesterday_end)
        self.time.append(yesterday_start)
        self.time.append(yesterday_end)
        tz = time.timezone
        if tz == -28800:
            return [int(time.mktime(time.strptime(x, '%Y-%m-%d %H:%M:%S')) * 1000) for x in
                    [yesterday_start, yesterday_end]]
        return [int(time.mktime(time.strptime(x, '%Y-%m-%d %H:%M:%S')) * 1000) + (-28800 - tz) * 1000 for x in
                [yesterday_start, yesterday_end]]

    def _generate_html(self):
        with open(self.log, 'wb') as fp:
            fp.write('<!DOCTYPE html><html><body> \
                              <h3>%s:<br> \
                              Tested Jenkins job:<a href="%s" target="_blank">%s</a><br><br><br> \
                              Daily Result Summary:<br><br> \
                              Execution time: %s--%s<br>Run Times: %s<br> \
                              Jenkins Fail Times: %s %s<br><br><br>' % (
                self.report, self.stress_link, self.stress_link, self.time[0], self.time[1], len(self.num), len(self.fail_list),
                self._generate_hyperlink(self.fail_list, False) or ''))
            self._write_data_to_html(fp, self.regression, 'Regression')
            self._write_data_to_html(fp, self.feature, 'New feature')
            self._write_data_to_html(fp, self.timeout, 'TimeOut')
            fp.write('</body>\n</html>')

    def _write_data_to_html(self, fp, container, mode):
        count = mode == 'Regression' and REGRESSION_GENERATOR or mode == 'New feature' \
                and FEATURE_GENERATOR or TIMEOUT_GENERATOR
        fp.write('<h3>%s Test Cases Summary:' % mode)
        fp.write('</h3><table border="1"><tr><th>Num</th><th>Suite Name</th><th>Case Name</th> \
                          <th>Result(pass/total)</th><th>Owner</th><th>Log Link</th></tr>')
        for name in sorted(container.keys()):
            ids = sorted(container[name]['failed'])
            owner = container[name]['owner']
            if ids:
                self.owner.append(owner)
            total = container[name]['total']
            result = '%s/%s' % (total - len(ids), total)
            ids_link = self._generate_hyperlink(ids)
            if not ids:
                fp.write('<tr><td>%s</td><td>%s</td><td>%s</td><td style="color:green">%s</td>\
                          <td>%s</td><td>%s</td></tr>\n'% (count.next(), name.split('/')[0], \
                          name.split('/')[-1], result, owner, ids_link or ''))
            else:
                fp.write('<tr><td>%s</td><td style="color:red">%s</td><td style="color:red">%s</td> \
                          <td style="color:red">%s</td><td >%s</td><td>%s</td></tr>\n' % (count.next(), \
                          name.split('/')[0], name.split('/')[-1], result, owner, ids_link or ''))

        fp.write('</table><br><br>')

    def _generate_hyperlink(self, ids, flag=True):
        ids_link = []
        for _id in ids:
            hyperlink = flag and self.stress_link + _id + '/robot/report/log.html' or self.stress_link + _id
            ids_link.append('<a href="%s" target="_blank">%s</a>' % (hyperlink, _id))
        return ids_link

    def _at_failed_case_owner(self):
        msg = ''
        for name in list(set(self.owner)):
            msg += '@' + name + ', '
        msg = '<font color="#FF0000">%s</font>' % msg + 'please help to check below failed cases.<br><br>'
        self._change_html_content(msg)

    def _at_ci_team(self):
        msg = '<font color="#FF0000">@CI Team</font>, please help to check jenkins failed job.<br><br>'
        self._change_html_content(msg)

    def _change_html_content(self, msg):
        with open(self.log, 'rb') as rp:
            content = rp.read()
        content = content.replace('Here is BTSMED', msg + 'Here is BTSMED', 1)
        with open(self.log, 'wb') as wp:
            wp.write(content)


def get_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def set_email_sent_list(sent, tag='to'):
    if not sent:
        sent = tag == 'to' and DEFAULT_TO or DEFAULT_CC
    return list(set([i for i in sent]))

def get_each_branch_info(branch):
    if branch.upper() == 'SRAN17A_P7':
        stress_link_trunk='http://hztdci01.china.nsn-net.net/job/IMP_SBTS17A_P7_STRESS_ET/'
        stress_link_resil = 'http://hztdci01.china.nsn-net.net/job/IMP_SBTS17A_P7_STRESS_ET_Resiliency/'
        trunk_report = 'Here is BTSMED 17A P7 Singleton stress testing report base on docker'
        resil_report = 'Here is BTSMED 17A P7 A-S stress testing report base on docker'
    elif branch.upper() == 'SRAN17A_MP':
        stress_link_trunk = 'http://hztdci01.china.nsn-net.net/job/IMP_17A_STRESS_ET/'
        stress_link_resil = 'http://hztdci01.china.nsn-net.net/job/IMP_17A_STRESS_ET_Feature3875/'
        trunk_report = 'Here is BTSMED 17A MP Singleton stress testing report base on docker'
        resil_report = 'Here is BTSMED 17A MP A-S stress testing report base on docker'
    elif branch.upper() == 'SRAN18':
        stress_link_trunk = 'http://hztdci01.china.nsn-net.net/job/IMP_xL18_STRESS_ET/'
        stress_link_resil = 'http://hztdci01.china.nsn-net.net/job/IMP_xL18_STRESS_ET_Resiliency/'
        trunk_report = 'Here is BTSMED 18 Singleton stress testing report base on docker'
        resil_report = 'Here is BTSMED 18 A-S stress testing report base on docker'
    elif branch.upper() == 'TRUNK':
        stress_link_trunk = 'http://hztdci01.china.nsn-net.net/job/IMP_GIT_TRUNK_STRESS_ET/'
        stress_link_resil = 'http://hztdci01.china.nsn-net.net/job/IMP_GIT_TRUNK_STRESS_ET_FOR_RESIL/'
        trunk_report = 'Here is BTSMED TRUNK Singleton stress testing report base on docker'
        resil_report = 'Here is BTSMED TRUNK A-S stress testing report base on docker'
    else:
        sys.stderr.write('%s\n' % __doc__)
        sys.exit()
    return stress_link_trunk, stress_link_resil, trunk_report, resil_report

class StressTest(Process):
    def __init__(self):
        Process.__init__(self)
        self.daemon = True

    def parse_start(self, tag, stress_line, log, report, flag):
        task = Parse(tag, stress_line, log, report, flag)
        task.start()


_StressTest = StressTest()

if __name__ == '__main__':
    kwargs = sys.argv[1:]
    if not kwargs or len(kwargs) > 4:
        sys.stderr.write('%s\n' % __doc__)
        sys.exit()
    branch = kwargs[0]
    args = kwargs[1:]

    to = ''
    cc = ''
    _flag = True

    if not args:
        pass
    elif len(args) == 1 and args[0] == 'debug':  #For debug mode
        _flag = False
    elif len(args) == 2 and args[0] in ['to', 'cc']:  #For to or cc mode
        to = args[0] == 'to' and args[1] or None
        cc = args[0] == 'cc' and args[1] or None
    elif len(args) == 3 and args[0] == 'to':# For to and cc mode
        to = args[1]
        cc = args[2]
    else:
        sys.stderr.write('%s\n' % __doc__)
        sys.exit()

    to = to and to.split(', ') or None
    cc = cc and cc.split(', ') or None
    TO_RECEIVERS = set_email_sent_list(to, tag='to')
    CC_RECEIVERS = set_email_sent_list(cc, tag='cc')
    stress_link_trunk, stress_link_resil, trunk_report, resil_report = get_each_branch_info(branch)

    log_trunk = os.path.join(os.path.abspath(os.path.dirname(__file__)), '%s_trunk.html' % branch.upper())
    log_resil = os.path.join(os.path.abspath(os.path.dirname(__file__)), '%s_resil.html' % branch.upper())
    _StressTest.parse_start('ET', stress_link_trunk, log_trunk, trunk_report, _flag)
    _StressTest.parse_start('Resiliency', stress_link_resil, log_resil, resil_report, _flag)

    if branch.upper() == 'TRUNK':
        stress_link_A_A_resil = 'http://hztdci01.china.nsn-net.net/job/IMP_GIT_TRUNK_STRESS_ET_FOR_A_A_RESIL/'
        A_A_resil_report = 'Here is BTSMED TRUNK A-A stress testing report base on docker'
        log_A_A_resil = os.path.join(os.path.abspath(os.path.dirname(__file__)), '%s_A_A_resil.html' % branch.upper())
        _StressTest.parse_start('Active-Active', stress_link_A_A_resil, log_A_A_resil, A_A_resil_report, _flag)
