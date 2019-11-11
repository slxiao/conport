

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

