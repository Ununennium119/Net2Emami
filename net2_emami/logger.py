from datetime import datetime
from enum import Enum

from print_color import print_color


class LogLevel(Enum):
    """
    An enumeration of log levels.

    This class represents the different levels of logging that can be used
    by the Logger class. Each level corresponds to a different severity of
    the logged messages.

    Attributes:
        ERROR (int): The error log level.
        WARN (int): The warning log level.
        SUCCESS (int): The success log level.
        INFO (int): The info log level.
        DEBUG (int): The debug log level.
    """

    ERROR = 1
    WARN = 2
    SUCCESS = 3
    INFO = 4
    DEBUG = 5


class Logger:
    """
    A singleton class for logging messages with different log levels.

    This class provides methods for logging messages at different levels:
    debug, success, info, warn, and error. Each method logs the message
    with a corresponding log level and color.

    Attributes:
        _instance (Logger): The singleton instance of the Logger class.
        Color (print_color.Color): The color enumeration from the print_color module.
    """

    _instance = None
    Color = print_color.Color

    def __init__(self):
        """
        Initializes the Logger instance.

        The log level is set to SUCCESS by default.
        """
        self._log_level = LogLevel.SUCCESS

    def __new__(cls):
        """
        Create a new Logger instance if one does not exist.

        This method overrides the __new__ method to implement the singleton pattern.
        If an instance of the Logger class does not exist, it creates one.
        Otherwise, it returns the existing instance.

        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    @property
    def log_level(self):
        """
        Get the current log level.

        Returns:
            LogLevel: The current log level.
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value: LogLevel):
        """
        Set the current log level.

        Args:
            value (LogLevel): The new log level.
        """
        self._log_level = value

    def error(self, message: str):
        """
        Log an error message.

        Args:
            message (str): The message to log.
        """
        if self.log_level >= LogLevel.ERROR:
            self._log(message, 'ERROR', 'red')

    def warn(self, message: str):
        """
        Log a warning message.

        Args:
            message (str): The message to log.
        """
        if self.log_level >= LogLevel.WARN:
            self._log(message, 'WARN', 'yellow')

    def success(self, message: str):
        """
        Log a success message.

        Args:
            message (str): The message to log.
        """
        if self.log_level >= LogLevel.SUCCESS:
            self._log(message, 'SUCCESS', 'green')

    def info(self, message: str):
        """
        Log an info message.

        Args:
            message (str): The message to log.
        """
        if self.log_level >= LogLevel.INFO:
            self._log(message, 'INFO', 'blue')

    def debug(self, message: str):
        """
        Log a debug message.

        Args:
            message (str): The message to log.
        """
        if self.log_level >= LogLevel.DEBUG:
            self._log(message, 'DEBUG', 'white')

    @staticmethod
    def _log(message: str, log_level: str, color: Color):
        """
        Log a message with a specified log type and color.

        This method logs the message with the specified log type and color.
        It uses the print_color module to print the message with the specified color.

        Args:
            message (str): The message to log.
            log_level (str): The log type of the message.
            color (Color): The color to use when printing the message.
        """
        print_color.print(
            f'{datetime.now()}\t\t{message}',
            tag=log_level,
            tag_color=color
        )
