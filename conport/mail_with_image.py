from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from datetime import date

import smtplib

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
        '''
        _msg = MIMEText('Hello\n\n%s\n%s' % (self._get_xml_content(), 'Best Regards'), 'html', 'utf-8')
        print(_msg)
        _msg['From'] = "shiliang-shelwin.xiao@nokia-sbell.com"
        _msg['To'] = ';'.join(["shiliang-shelwin.xiao@nokia-sbell.com", "slxiao1988@163.com", "shliangxiao@gmail.com"])
        _msg['Cc'] = ';'.join(["slxiao1988@163.com", "shliangxiao@gmail.com"])
        _msg['Subject'] = '[%s] %s' % (date.today(), self.report)
        '''

        msg = MIMEMultipart('related')
        msg['From'] = "shiliang-shelwin.xiao@nokia-sbell.com"
        msg['To'] = ';'.join(["shiliang-shelwin.xiao@nokia-sbell.com", "slxiao1988@163.com", "shliangxiao@gmail.com"])
        msg['Cc'] = ';'.join(["slxiao1988@163.com", "shliangxiao@gmail.com"])
        msg['Subject'] = '[%s] %s' % (date.today(), self.report)

        html = """\
            <html>
                <head></head>
            <body>
                <img src="cid:image1" alt="Logo" style="width:250px;height:50px;"><br>
                <p><h4 style="font-size:15px;">Some Text.</h4></p>           
            </body>
            </html>
        """
        # Record the MIME types of text/html.
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        msg.attach(part2)

            # This example assumes the image is in the current directory
        fp = open('logo.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        #   Define the image's ID as referenced above
        msgImage.add_header('Content-ID', '<image1>')
        msg.attach(msgImage)
        self._msg = msg

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
            print "INFO: Sent email successfully!"
        except smtplib.SMTPException as e:
            raise RuntimeError("ERROR: Can not send email. Error is %s." % str(e))

if __name__ == "__main__":
    SentEmail("Here is the report of xxx", "output.html").run()

