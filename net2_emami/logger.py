from datetime import datetime
from enum import Enum
from pathlib import Path

from print_color import print_color


class LogLevel(Enum):
    """
    Enumeration of log levels.

    Attributes:
        NO_LOG: No logging.
        ERROR: Log errors.
        WARN: Log warnings.
        SUCCESS: Log success messages.
        INFO: Log informational messages.
        DEBUG: Log debug messages.
    """
    NO_LOG = 0
    ERROR = 1
    WARN = 2
    SUCCESS = 3
    INFO = 4
    DEBUG = 5


class Logger:
    """
    Singleton class for logging.

    Attributes:
        _instance: Instance of the Logger class.
        Color: Color enumeration for print_color.

    Methods:
        __init__: Initialize the Logger instance.
        __new__: Create a new Logger instance.
        log_level: Getter and setter for the log level.
        write_to_file: Getter and setter for whether to write to a file.
        stop: Stop the logger and delete the log file if it is not needed.
        error: Log an error message.
        warn: Log a warning message.
        success: Log a success message.
        info: Log an informational message.
        debug: Log a debug message.
        _log: Log a message with a given level and color.
    """

    _instance = None
    Color = print_color.Color

    def __init__(self):
        """
        Initialize the Logger instance.

        The log level is set to SUCCESS by default,
        and it logs to a file with a name based on the current date and time.
        """
        self._log_level: LogLevel = LogLevel.SUCCESS
        self._write_to_file: bool = False
        self._log_file_path: str = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_log.txt'
        self._log_file = open(self._log_file_path, 'w')

    def __new__(cls):
        """
        Create a new Logger instance.

        If the Logger instance already exists, it returns the existing instance.
        """
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    @property
    def log_level(self) -> LogLevel:
        """
        Getter for the log level.

        Returns:
            LogLevel: The current log level.
        """
        return self._log_level

    @log_level.setter
    def log_level(self, value: LogLevel):
        """
        Setter for the log level.

        Args:
            value (LogLevel): The new log level.
        """
        self._log_level = value

    @property
    def write_to_file(self) -> bool:
        """
        Getter for whether to write to a file.

        Returns:
            bool: Whether to write to a file.
        """
        return self._write_to_file

    @write_to_file.setter
    def write_to_file(self, value: bool):
        """
        Setter for whether to write to a file.

        Args:
            value (bool): Whether to write to a file.
        """
        self._write_to_file = value

    def stop(self):
        """
        Stop the logger and delete the log file if it is not needed.
        """
        if not self._log_file.closed:
            self._log_file.flush()
            self._log_file.close()
        if not self._write_to_file:
            path = Path(self._log_file_path)
            path.unlink(missing_ok=True)

    def error(self, message: str):
        """
        Log an error message.

        Args:
            message (str): The error message.
        """
        if self.log_level.value >= LogLevel.ERROR.value:
            self._log(message, 'ERROR', 'red')

    def warn(self, message: str):
        """
        Log a warning message.

        Args:
            message (str): The warning message.
        """
        if self.log_level.value >= LogLevel.WARN.value:
            self._log(message, 'WARN', 'yellow')

    def success(self, message: str):
        """
        Log a success message.

        Args:
            message (str): The success message.
        """
        if self.log_level.value >= LogLevel.SUCCESS.value:
            self._log(message, 'SUCCESS', 'green')

    def info(self, message: str):
        """
        Log an informational message.

        Args:
            message (str): The informational message.
        """
        if self.log_level.value >= LogLevel.INFO.value:
            self._log(message, 'INFO', 'blue')

    def debug(self, message: str):
        """
        Log a debug message.

        Args:
            message (str): The debug message.
        """
        if self.log_level.value >= LogLevel.DEBUG.value:
            self._log(message, 'DEBUG', 'white')

    def _log(self, message: str, log_level: str, color: Color):
        """
        Log a message with a given level and color.

        Args:
            message (str): The message to log.
            log_level (str): The level of the message.
            color (Color): The color of the message.
        """
        log = f'{datetime.now()}\t\t{message}'
        print_color.print(
            log,
            tag=log_level,
            tag_color=color
        )
        if self._write_to_file and not self._log_file.closed:
            self._log_file.write(f'{log}\n')
