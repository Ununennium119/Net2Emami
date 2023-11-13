import time

import requests

from net2_emami.logger import Logger


class Net2Emami:
    """
    The Net2Emami class is used to manage login and logout operations on the net2.sharif.edu website.

    Attributes:
        logger (Logger): An instance of the Logger class used for logging.
        LOGIN_URL (str): The URL for the login operation.
        LOGOUT_URL (str): The URL for the logout operation.
        username (str): The username for the login operation.
        password (str): The password for the login operation.
        login_retry_seconds (float): The number of seconds to wait before retrying the login operation.
        logout_retry_seconds (float): The number of seconds to wait before retrying the logout operation.
        cycle_seconds (float): The number of seconds to wait before starting the next cycle of login and logout operations.
    """
    logger = Logger()

    LOGIN_URL = 'https://net2.sharif.edu/login'
    LOGOUT_URL = 'https://net2.sharif.edu/logout'

    def __init__(
            self,
            credentials_path: str,
            login_retry_seconds: float,
            logout_retry_seconds: float,
            cycle_seconds: float
    ):
        """
        Constructs a new Net2Emami object.

        Args:
            credentials_path (str): The path to the file containing the username and password.
            login_retry_seconds (float): The number of seconds to wait before retrying the login operation.
            logout_retry_seconds (float): The number of seconds to wait before retrying the logout operation.
            cycle_seconds (float): The number of seconds to wait before starting the next cycle of login and logout operations.
        """
        with open(credentials_path, 'r') as credentials_file:
            self.username: str = credentials_file.readline().strip()
            self.password: str = credentials_file.readline().strip()
        self.login_retry_seconds: float = login_retry_seconds
        self.logout_retry_seconds: float = logout_retry_seconds
        self.cycle_seconds: float = cycle_seconds

    def run(self):
        """
        Starts the infinite loop of login and logout operations.
        """
        while True:
            while not self._logout():
                time.sleep(self.logout_retry_seconds)
            while not self._login():
                time.sleep(self.login_retry_seconds)
            time.sleep(self.cycle_seconds)

    def _login(self) -> bool:
        """
        Logs in to the net2.sharif.edu website.

        Returns:
            bool: True if the login operation was successful, False otherwise.
        """
        body = {
            'username': self.username,
            'password': self.password
        }
        try:
            self.logger.info('Sending login request...')
            response = requests.post(url=self.LOGIN_URL, data=body)
        except Exception:
            self.logger.error('Login failed')
            return False
        if response.status_code != 200:
            self.logger.error('Login failed')

        self.logger.success('Login successful')
        return response.status_code == 200

    def _logout(self) -> bool:
        """
        Logs out from the net2.sharif.edu website.

        Returns:
            bool: True if the logout operation was successful, False otherwise.
        """
        try:
            self.logger.info('Sending logout request...')
            response = requests.get(url=self.LOGOUT_URL)
        except Exception:
            self.logger.error('Logout failed')
            return False
        if response.status_code != 200:
            self.logger.error('Logout failed')

        self.logger.success('Logout successful')
        return response.status_code == 200
