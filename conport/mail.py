from datetime import date
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage

from .summary import get_build_summary
from .figure import get_binary_figure


class SendEmail(object):
    def __init__(self, host, user, password, title, _from, to, cc, html_output, build_summary, pure_html):
        self.mail_host = host
        self.mail_user = user
        self.mail_password = password
        self.msg = None
        self.title = title
        self.pure_html = pure_html
        self.html_output = html_output
        self._from = _from
        self.to = to
        self.cc = cc
        self.build_summary = build_summary
        self.run()

    def run(self):
        self._generate_mail_text()
        self._send_email()

    def _generate_mail_text(self):
        if self.pure_html == "true":
            msg = MIMEText(self.html_output, 'html', 'utf-8')
        else:
            msg = MIMEMultipart('related')
            msg.attach(MIMEText(self.html_output, 'html'))
            msgImage = MIMEImage(get_binary_figure(self.build_summary), "png")
            msgImage.add_header('Content-ID', '<build_summary_image>')
            msg.attach(msgImage)
        msg['From'] = self._from
        msg['To'] = ';'.join(self.to)
        msg['Cc'] = ';'.join(self.cc)
        msg['Subject'] = '[%s] %s' % (date.today(), self.title)
        self.msg = msg

    def _send_email(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self.mail_host, 25)
            try:
                smtpobj.login(self.mail_user, self.mail_password)
            except Exception:
                print("login fail, ignore.....")
                pass
            smtpobj.sendmail(self.msg['From'], (self.msg['To'] + ';' + self.msg['Cc']).split(';'),
                             self.msg.as_string())
            smtpobj.quit()
            print("sent email successfully!")
        except smtplib.SMTPException as e:
            raise RuntimeError(
                "can not send email. error is %s." % str(e))
