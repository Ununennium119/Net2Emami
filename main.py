import datetime
import time
import typing

import requests
from print_color import print

Color = typing.Literal[
    "purple",
    "blue",
    "green",
    "yellow",
    "red",
    "magenta",
    "yan",
    "black",
    "white",
    "v",
    "p",
    "b",
    "g",
    "y",
    "r",
    "m",
    "c",
    "k",
    "w",
]


def main():
    net2_emami = Net2Emami(
        'credentials',
        0.25,
        0.25,
        30
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
        while not self._login():
            time.sleep(self.login_retry_seconds)
        while True:
            time.sleep(self.cycle_seconds)
            while not self._logout():
                time.sleep(self.logout_retry_seconds)
            while not self._login():
                time.sleep(self.login_retry_seconds)

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
        print(
            f'{datetime.datetime.now()}\t\t{message}',
            tag=tag.name,
            tag_color=tag.color
        )


if __name__ == '__main__':
    main()
