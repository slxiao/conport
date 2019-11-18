from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from datetime import date

import smtplib
from report import get_html_output

from figure import get_binary_figure

class SentEmail(object):
    def __init__(self, report, log, html5):
        self._mail_host = 'mailrelay.int.nokia.com'
        self._mail_user = 'tdd_lte_oam_ci'
        self._mail_password = ''
        self._msg = None
        self._log = log
        self.report = report
        self.html5 = html5

    def run(self):
        self._generate_mail_text()
        self._sent_email()

    def _generate_mail_text(self):
        html_output = get_html_output(self.html5)
        if self.html5:
            msg = MIMEText(html_output, 'html', 'utf-8')            
        else:
            msg = MIMEMultipart('related')
            # Record the MIME types of text/html.
            part2 = MIMEText(html_output, 'html')

            # Attach parts into message container.
            msg.attach(part2)

            # This example assumes the image is in the current directory
            msgImage = MIMEImage(get_binary_figure(), "png")

            #   Define the image's ID as referenced above
            msgImage.add_header('Content-ID', '<build_trend_image>')
            msg.attach(msgImage)
        msg['From'] = "shiliang-shelwin.xiao@nokia-sbell.com"
        msg['To'] = ';'.join(["shiliang-shelwin.xiao@nokia-sbell.com", "slxiao1988@163.com", "shliangxiao@gmail.com"])
        msg['Cc'] = ';'.join(["slxiao1988@163.com", "shliangxiao@gmail.com"])
        msg['Subject'] = '[%s] %s' % (date.today(), self.report)
        self.msg = msg

    def _sent_email(self):
        try:
            smtpobj = smtplib.SMTP()
            smtpobj.connect(self._mail_host, 25)
            try:
                smtpobj.login(self._mail_user, self._mail_password)
            except Exception:
                pass
            smtpobj.sendmail(self.msg['From'], (self.msg['To'] + ';' + self.msg['Cc']).split(';'),
                             self.msg.as_string())
            smtpobj.quit()
            print "INFO: Sent email successfully!"
        except smtplib.SMTPException as e:
            raise RuntimeError("ERROR: Can not send email. Error is %s." % str(e))

if __name__ == "__main__":
    SentEmail("Here is the report of xxx", "output.html", True).run()

