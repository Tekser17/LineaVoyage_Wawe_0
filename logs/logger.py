import json
import time
import logging
import os.path
import datetime
from typing import Any
from functools import wraps
from globals import PROJECT_PATH

with open('config.json', 'r') as config_file:
    config = json.loads(config_file.read())

project_dir = PROJECT_PATH



logging_config = config['logging']


class Logger:
    formatter = logging.Formatter('%(asctime)s - %(levelname)s %(message)s')

    def __init__(self, filename: str):
        if logging_config['level'] == "info":
            level = logging.INFO
        elif logging_config['level'] == "debug":
            level = logging.DEBUG
        else:
            raise Exception('Logging level is not configured in config.json')

        logger = logging.getLogger('my_logger')
        self.__logger = logger
        self.__is_time_measuring = False
        self.__start_time = None

        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        console_handler.setLevel(logging.DEBUG)

        today = datetime.date.today()
        day = today.day
        month = today.month
        year = today.year

        log_path = f'{project_dir}/logs/{year}-{day}-{month}-{filename}.log'
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(level)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        self.__file_handler = file_handler
        self.__console_handler = console_handler

    @property
    def _is_time_measuring(self):
        return self.__is_time_measuring

    @_is_time_measuring.setter
    def _is_time_measuring(self, value: bool):
        if isinstance(value, bool):
            self.__is_time_measuring = value

    @staticmethod
    def __check_enabling(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            if logging_config['enable']:
                return func(self, *args, **kwargs)

        return wrapper

    @__check_enabling
    def time_execution(self, label: str = 'Code') -> None:
        if not self._is_time_measuring:
            self.__start_time = time.monotonic()
            self._is_time_measuring = True
        elif self._is_time_measuring:
            start_time = self.__start_time
            end_time = time.monotonic()
            elapsed_time = end_time - start_time
            self._is_time_measuring = False
            self.__logger.debug(f"{label} took {elapsed_time:.6f} seconds")

    @__check_enabling
    def only_message(self, message: str):
        logging.Formatter('%(message)s')
        logging.info(message)
        logging.Formatter(self.formatter)

    @__check_enabling
    def debug(self, message: str):
        self.__logger.debug(message)

    @__check_enabling
    def info(self, message: str):
        self.__logger.info(message)

    @__check_enabling
    def exception(self, message, err: Exception = None):
        message += ': %s'
        self.__logger.exception(message, err)

    @__check_enabling
    def error(self, message: str):
        self.__logger.error(message)

    @__check_enabling
    def critical(self, message: str):
        self.__logger.critical(message)

    @__check_enabling
    def only_message(self, message: str):
        temp_formatter = logging.Formatter('%(message)s')
        self.__file_handler.setFormatter(temp_formatter)
        self.__console_handler.setFormatter(temp_formatter)
        self.__logger.info(message)
        self.__file_handler.setFormatter(self.formatter)
        self.__console_handler.setFormatter(self.formatter)
