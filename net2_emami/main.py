import argparse

from net2_emami.net2_emami import Net2Emami


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
        default="0.25"
    )
    parser.add_argument(
        '-or', '--logout-retry',
        action="store",
        dest="logout_retry",
        type=float,
        help="The seconds between retries for logout",
        default="0.25"
    )
    parser.add_argument(
        '-y', '--cycle',
        action="store",
        dest="cycle",
        type=float,
        help="The seconds between each logout-login",
        default="30"
    )

    args = parser.parse_args()
    credentials = args.credentials
    login_retry = float(args.login_retry)
    logout_retry = float(args.logout_retry)
    cycle = float(args.cycle)

    net2_emami = Net2Emami(
        credentials,
        login_retry,
        logout_retry,
        cycle
    )
    net2_emami.run()


if __name__ == '__main__':
    main()
