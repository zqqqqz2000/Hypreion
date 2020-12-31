import colorama

from core.core_types import Logger
from colorama import init, Fore, Back, Style
from typing import *
import time

colorama.init(True)


class Echo(Logger):
    @staticmethod
    def error(src: Any, information: str) -> NoReturn:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(Fore.RED + f'[{t} {src}] {information}')

    @staticmethod
    def warning(src: Any, information: str) -> NoReturn:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(Fore.YELLOW + f'[{t} {src}] {information}')

    @staticmethod
    def information(src: Any, information: str) -> NoReturn:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(Fore.GREEN + f'[{t} {src}] {information}')

    @staticmethod
    def debug(src: Any, information: str) -> NoReturn:
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(Fore.BLUE + f'[{t} {src}] /DEBUG/ {information}')
