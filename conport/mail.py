from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from datetime import date

import smtplib

from .figure import get_binary_figure


class SendEmail(object):
    def __init__(self, host, user, password, title, _from, to, cc, html_output, html5):
        print(host, user, password, title, _from, to, cc)
        self.mail_host = host
        self.mail_user = user
        self.mail_password = password
        self.msg = None
        self.title = title
        self.html5 = html5
        self.html_output = html_output
        self._from = _from
        self.to = to
        self.cc = cc
        self.run()

    def run(self):
        self._generate_mail_text()
        self._sent_email()

    def _generate_mail_text(self):
        if self.html5 == "true":
            msg = MIMEText(self.html_output, 'html', 'utf-8')
        else:
            msg = MIMEMultipart('related')
            # Record the MIME types of text/html.
            part2 = MIMEText(self.html_output, 'html')
            # Attach parts into message container.
            msg.attach(part2)
            # This example assumes the image is in the current directory
            msgImage = MIMEImage(get_binary_figure(), "png")
            #   Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<build_trend_image>')
            msg.attach(msgImage)

        msg['From'] = self._from
        msg['To'] = ';'.join(self.to)
        msg['Cc'] = ';'.join(self.cc)
        msg['Subject'] = '[%s] %s' % (date.today(), self.title)
        self.msg = msg

    def _sent_email(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self.mail_host, 25)
            try:
                smtpobj.login(self.mail_user, self.mail_password)
            except Exception:
                pass
            smtpobj.sendmail(self.msg['From'], (self.msg['To'] + ';' + self.msg['Cc']).split(';'),
                             self.msg.as_string())
            smtpobj.quit()
            print "INFO: Sent email successfully!"
        except smtplib.SMTPException as e:
            raise RuntimeError(
                "ERROR: Can not send email. Error is %s." % str(e))
