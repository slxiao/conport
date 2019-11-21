import argparse

from .config import get_default_config


def get_parser():
    defaults = get_default_config()

    parser = argparse.ArgumentParser()

    parser.add_argument("--job_url", help="Jenkins job url",
                        default=defaults.default.job_url)
    parser.add_argument("--report_title", help="continuous testing report title",
                        default=defaults.default.report_title)
    parser.add_argument("--past_hours", help="number of past hours to be monitored",
                        type=int, default=defaults.default.past_hours)

    parser.add_argument("--send_email", help="whether to send email or not",
                        default=defaults.email.send_email)
    parser.add_argument("--mail_host", help="email host",
                        default=defaults.email.mail_host)
    parser.add_argument("--mail_user", help="email user",
                        default=defaults.email.mail_user)
    parser.add_argument("--mail_pwd", help="email password",
                        default=defaults.email.mail_pwd)
    parser.add_argument("--sender", help="email sender",
                        default=defaults.email.sender)
    parser.add_argument(
        "--receivers", help="email receivers, format is receiver1, receiver2, ...", default=defaults.email.receivers)
    parser.add_argument("--receivers_cc",
                        help="email receivers cc, format is receivercc1, receivercc2, ...", default=defaults.email.receivers_cc)

    parser.add_argument("--pure_html", help="pure html or not",
                        default=defaults.default.pure_html)

    parser.add_argument("--report_lan", help="report langurage, english or chinese, default is english",
                        default=defaults.default.report_lan)

    parser.add_argument("--version", action='store_true', help="print version")

    return parser
