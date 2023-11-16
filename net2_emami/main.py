import argparse
import signal
import threading

from logger import LogLevel
from auto_login import AutoLogin


def main():
    parser = argparse.ArgumentParser(
        prog='Net2 Emami',
        description='This program enables you to use Net2 without limitations'
    )
    parser.add_argument(
        '-c', '--credentials',
        action="store",
        dest="credentials",
        help="The file containing the username in its first line and the password in its second line.",
        default="credentials"
    )
    parser.add_argument(
        '-ir', '--login-retry',
        action="store",
        dest="login_retry",
        type=float,
        help="The seconds between retries for login",
        default=0.25
    )
    parser.add_argument(
        '-or', '--logout-retry',
        action="store",
        dest="logout_retry",
        type=float,
        help="The seconds between retries for logout",
        default=0.25
    )
    parser.add_argument(
        '-y', '--cycle',
        action="store",
        dest="cycle",
        type=float,
        help="The seconds between each logout-login",
        default=30
    )
    parser.add_argument(
        '-l', '--log-level',
        action="store",
        dest="log_level",
        type=int,
        choices=list(range(6)),
        help="Log level (NO_LOG = 0, ERROR = 1 WARN = 2 SUCCESS = 3 INFO = 4 DEBUG = 5)",
        default=4
    )
    parser.add_argument(
        '-lf', '--log-file',
        action="store_true",
        dest="log_file",
        help="If present, a log file will be created",
        default=False
    )

    args = parser.parse_args()
    credentials = args.credentials
    login_retry = float(args.login_retry)
    logout_retry = float(args.logout_retry)
    cycle = float(args.cycle)
    log_level = LogLevel(args.log_level)
    log_file = args.log_file

    auto_login = AutoLogin(
        credentials,
        login_retry,
        logout_retry,
        cycle,
        log_level,
        log_file
    )
    auto_login.run()


if __name__ == '__main__':
    main()
