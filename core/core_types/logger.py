from typing import *

from core.core_errors.logger_errors import LoggerTypeUndefined


class Logger:
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFORMATION = 'INFORMATION'
    DEBUG = 'DEBUG'

    @classmethod
    def log(cls, log_type: str, src: Any, information: str) -> NoReturn:
        method_mapper = {
            cls.ERROR: cls.error,
            cls.WARNING: cls.warning,
            cls.INFORMATION: cls.information,
            cls.DEBUG: cls.debug
        }

        if log_type not in method_mapper:
            raise LoggerTypeUndefined()
        else:
            method_mapper[log_type](src, information)

    @staticmethod
    def error(src: Any, information: str) -> NoReturn:
        ...

    @staticmethod
    def warning(src: Any, information: str) -> NoReturn:
        ...

    @staticmethod
    def information(src: Any, information: str) -> NoReturn:
        ...

    @staticmethod
    def debug(src: Any, information: str) -> NoReturn:
        ...
