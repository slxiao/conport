from .argument import get_parser
from .build import get_test_reports
from .summary import get_build_summary
from .summary import get_case_summary
from .report import get_html_output
from .mail import SendEmail
from . import __version__


def conport(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    if args.version:
        print("conport v" + __version__)
        return

    test_reports = get_test_reports(args.job_url, args.past_hours)
    if not test_reports:
        print("no valie test reports, exit")
        return
    build_summary = get_build_summary(test_reports)
    case_summary = get_case_summary(test_reports)

    html_output = get_html_output(
        args.job_url, args.report_title, args.past_hours, build_summary, case_summary, args.pure_html)
    if args.send_email == "true":
        SendEmail(args.mail_host, args.mail_user, args.mail_pwd, args.report_title, args.sender,
                  args.receivers, args.receivers_cc, html_output, build_summary, args.pure_html)


if __name__ == "__main__":
    conport()
