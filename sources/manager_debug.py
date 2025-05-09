from datetime import datetime
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL, getLogger, Logger, StreamHandler, Formatter
from string import Template
from typing import Dict
from os import environ

from humanize import precisedelta

from manager_environment import EnvironmentManager as EM
from manager_file import FileManager as FM


def init_debug_manager():
    """
    Initialize download manager:
    - Setup headers for GitHub GraphQL requests.
    - Launch static queries in background.
    """
    DebugManager.create_logger()


class DebugManager:
    """
    Class for handling debug logging.
    """

    _logger = None

    _COLOR_RESET = "\u001B[0m"
    _COLOR_RED = "\u001B[31m"
    _COLOR_GREEN = "\u001B[32m"
    _COLOR_BLUE = "\u001B[34m"
    _COLOR_YELLOW = "\u001B[33m"

    _DATE_TEMPLATE = "date"
    _TIME_TEMPLATE = "time"

    @staticmethod
    def create_logger(level: int = DEBUG) -> None:
        """
        Create logger with specified level.
        :param level: Logging level.
        """
        DebugManager._logger = getLogger("waka-readme-stats")
        DebugManager._logger.setLevel(level)

        handler = StreamHandler()
        handler.setFormatter(Formatter("%(message)s"))
        DebugManager._logger.addHandler(handler)

    @staticmethod
    def _process_template(message: str, kwargs: Dict) -> str:
        if DebugManager._DATE_TEMPLATE in kwargs:
            kwargs[DebugManager._DATE_TEMPLATE] = f"{datetime.strftime(kwargs[DebugManager._DATE_TEMPLATE], '%d-%m-%Y %H:%M:%S:%f')}"
        if DebugManager._TIME_TEMPLATE in kwargs:
            kwargs[DebugManager._TIME_TEMPLATE] = precisedelta(kwargs[DebugManager._TIME_TEMPLATE], minimum_unit="microseconds")

        return Template(message).substitute(kwargs)

    @staticmethod
    def g(message: str, **kwargs):
        message = DebugManager._process_template(message, kwargs)
        DebugManager._logger.info(f"{DebugManager._COLOR_GREEN}{message}{DebugManager._COLOR_RESET}")

    @staticmethod
    def i(message: str, **kwargs):
        message = DebugManager._process_template(message, kwargs)
        DebugManager._logger.debug(f"{DebugManager._COLOR_BLUE}{message}{DebugManager._COLOR_RESET}")

    @staticmethod
    def w(message: str, **kwargs):
        message = DebugManager._process_template(message, kwargs)
        DebugManager._logger.warning(f"{DebugManager._COLOR_YELLOW}{message}{DebugManager._COLOR_RESET}")

    @staticmethod
    def p(message: str, **kwargs):
        message = DebugManager._process_template(message, kwargs)
        DebugManager._logger.error(message)
