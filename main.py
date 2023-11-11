import argparse
import datetime
import time

import print_color
import requests

Color = print_color.print_color.Color


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


class Net2Emami:
    class LogTag:
        def __init__(self, name: str, color: Color):
            self.name: str = name
            self.color: Color = color

    infoTag = LogTag('INFO', 'blue')
    warnTag = LogTag('WARN', 'yellow')

    def __init__(
            self,
            credentials_path: str,
            login_retry_seconds: float,
            logout_retry_seconds: float,
            cycle_seconds: float
    ):
        with open(credentials_path, 'r') as credentials_file:
            self.username: str = credentials_file.readline().strip()
            self.password: str = credentials_file.readline().strip()
        self.login_url: str = 'https://net2.sharif.edu/login'
        self.logout_url: str = 'https://net2.sharif.edu/logout'
        self.login_retry_seconds: float = login_retry_seconds
        self.logout_retry_seconds: float = logout_retry_seconds
        self.cycle_seconds: float = cycle_seconds

    def run(self):
        while True:
            while not self._logout():
                time.sleep(self.logout_retry_seconds)
            while not self._login():
                time.sleep(self.login_retry_seconds)
            time.sleep(self.cycle_seconds)

    def _login(self) -> bool:
        """Log in to net2.

        :return: :class:`bool` True if successful
        """
        body = {
            'username': self.username,
            'password': self.password
        }
        try:
            self._log('Sending login request...', self.infoTag)
            response = requests.post(url=self.login_url, data=body)
        except Exception:
            self._log('Login failed', self.warnTag)
            return False
        if response.status_code != 200:
            self._log('Login failed', self.warnTag)

        self._log('Login successful', self.infoTag)
        return response.status_code == 200

    def _logout(self) -> bool:
        """Log out from net2.

        :return: :class:`bool` True if successful
        """
        try:
            self._log('Sending logout request...', self.infoTag)
            response = requests.get(url=self.logout_url)
        except Exception:
            self._log('Logout failed', self.warnTag)
            return False
        if response.status_code != 200:
            self._log('Logout failed', self.warnTag)

        self._log('Logout successful', self.infoTag)
        return response.status_code == 200

    @staticmethod
    def _log(message: str, tag: LogTag):
        print_color.print(
            f'{datetime.datetime.now()}\t\t{message}',
            tag=tag.name,
            tag_color=tag.color
        )


if __name__ == '__main__':
    main()
