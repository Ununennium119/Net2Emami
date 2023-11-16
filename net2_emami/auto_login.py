import time
import requests
from logger import Logger, LogLevel


class AutoLogin:
    """
    AutoLogin is a class designed to automatically login and logout from a network.

    Attributes:
        LOGIN_URL (str): The URL for the login operation.
        LOGOUT_URL (str): The URL for the logout operation.
        _running (bool): A flag to control the running state of the script.
        username (str): The username for the login operation.
        password (str): The password for the login operation.
        login_retry_seconds (float): The number of seconds to wait before retrying the login operation.
        logout_retry_seconds (float): The number of seconds to wait before retrying the logout operation.
        cycle_seconds (float): The number of seconds to wait before the next cycle of login and logout operations.
        logger (Logger): An instance of the Logger class for logging.
    """

    LOGIN_URL = 'https://net2.sharif.edu/login'
    LOGOUT_URL = 'https://net2.sharif.edu/logout'

    def __init__(
            self,
            credentials_path: str,
            login_retry_seconds: float,
            logout_retry_seconds: float,
            cycle_seconds: float,
            log_level: LogLevel,
            log_file: bool
    ):
        """
        Constructs an instance of the AutoLogin class.

        Parameters:
            credentials_path (str): The path to the file containing the username and password.
            login_retry_seconds (float): The number of seconds to wait before retrying the login operation.
            logout_retry_seconds (float): The number of seconds to wait before retrying the logout operation.
            cycle_seconds (float): The number of seconds to wait before the next cycle of login and logout operations.
            log_level (LogLevel): The level of logging for the Logger instance.
            log_file (bool): A flag to control whether to write logs to a file.
        """
        self._running: bool = True
        with open(credentials_path, 'r') as credentials_file:
            self.username: str = credentials_file.readline().strip()
            self.password: str = credentials_file.readline().strip()
        self.login_retry_seconds: float = login_retry_seconds
        self.logout_retry_seconds: float = logout_retry_seconds
        self.cycle_seconds: float = cycle_seconds

        self.logger = Logger()
        self.logger.log_level = log_level
        self.logger.write_to_file = log_file

    def run(self):
        """
        Starts the infinite loop of login and logout operations.

        This method starts the main loop of the AutoLogin class.
        It will keep running until the script is stopped manually.
        The loop will first attempt to log out, then wait for a specified number of seconds, then attempt to log in,
         and finally wait for another specified number of seconds before repeating the process.
        """
        self.logger.info("Press Ctrl+C to stop the script.")
        try:
            while self._running:
                while self._running and not self._logout():
                    time.sleep(self.logout_retry_seconds)
                while self._running and not self._login():
                    time.sleep(self.login_retry_seconds)
                time.sleep(self.cycle_seconds)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            raise e
        finally:
            self.stop()

    def stop(self):
        """
        Stops the script and logs the event.

        This method stops the main loop of the AutoLogin class and logs the event. It also stops the Logger instance.
        """
        self.logger.info('Stopping script...')
        self.logger.stop()
        self._running = False

    def _login(self) -> bool:
        """
        Attempts to log in to the network.

        This method sends a POST request to the LOGIN_URL with the username and password as data.
        If the request is successful and the response status code is 200, it logs a success message and returns True.
        If the request fails or the response status code is not 200, it logs an error message and returns False.

        Returns:
            bool: True if the login is successful, False otherwise.
        """
        body = {
            'username': self.username,
            'password': self.password
        }
        try:
            self.logger.info('Sending login request...')
            response = requests.post(url=self.LOGIN_URL, data=body, timeout=2)
        except Exception:
            self.logger.error('Login failed')
            return False
        if response.status_code != 200:
            self.logger.error('Login failed')

        self.logger.success('Login successful')
        return response.status_code == 200

    def _logout(self) -> bool:
        """
        Attempts to log out from the network.

        This method sends a GET request to the LOGOUT_URL.
        If the request is successful and the response status code is 200, it logs a success message and returns True.
        If the request fails or the response status code is not 200, it logs an error message and returns False.

        Returns:
            bool: True if the logout is successful, False otherwise.
        """
        try:
            self.logger.info('Sending logout request...')
            response = requests.get(url=self.LOGOUT_URL, timeout=2)
        except Exception:
            self.logger.error('Logout failed')
            return False
        if response.status_code != 200:
            self.logger.error('Logout failed')

        self.logger.success('Logout successful')
        return response.status_code == 200
