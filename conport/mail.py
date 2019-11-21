from datetime import date
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from .summary import get_build_summary
from .figure import get_binary_figure


class SendEmail(object):
    def __init__(self, host, user, password, title, _from, to, cc, html_output, build_summary, pure_html):
        self.mail_host = host
        self.mail_user = user
        self.mail_password = password
        self.msg = None
        self._from = _from
        self.to = ';'.join([i.strip() for i in to.strip().split(",")])
        self.cc = ';'.join([i.strip() for i in cc.strip().split(",")])
        self.title = '[%s] %s' % (date.today(), title)
        self.pure_html = pure_html
        self.html_output = html_output
        self.build_summary = build_summary
        self.run()

    def run(self):
        self._generate_mail_text()
        self._send_email()

    def update_msg(self):
        self.msg["From"] = self._from
        self.msg["To"] = self.to
        self.msg["Cc"] = self.cc
        self.msg["Subject"] = self.title

    def _generate_mail_text(self):
        if self.pure_html == "true":
            msg = MIMEText(self.html_output, 'html', 'utf-8')
        else:
            msg = MIMEMultipart('related')
            msg.attach(MIMEText(self.html_output, 'html'))
            msgImage = MIMEImage(get_binary_figure(self.build_summary), "png")
            msgImage.add_header('Content-ID', '<build_summary_image>')
            msg.attach(msgImage)
        self.msg = msg
        self.update_msg()

    def _send_email(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self.mail_host, 25)
            try:
                smtpobj.login(self.mail_user, self.mail_password)
            except Exception:
                print("login fail, ignore.....")
                pass
            print(self.msg['From'], self.msg['To'], self.msg['Cc'])
            smtpobj.sendmail(self.msg['From'], (self.msg['To'] + ';' + self.msg['Cc']).split(';'),
                             self.msg.as_string())
            smtpobj.quit()
            print("sent email successfully!")
        except smtplib.SMTPException as e:
            raise RuntimeError(
                "can not send email. error is %s." % str(e))
