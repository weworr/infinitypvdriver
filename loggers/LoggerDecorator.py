import os
from os import sep
from pathlib import Path
from datetime import datetime


def function_logger(func: callable) -> callable:
    def wrapper(*args: any, **kwargs: any) -> callable:
        file_path: str = str(Path(__file__).resolve().parent.parent) + sep + 'log.txt'

        with open(file_path, 'a') as file:
            file.write(f'{datetime.now()} Function: {func.__name__}, arguments: {args}\n')

        result = func(*args, **kwargs)
        with open(file_path, 'a') as file:
            file.write(f'{datetime.now()} Result: {result}\n')

        return result

    return wrapper


def command_logger(func: callable) -> callable:
    def wrapper(*args: any, **kwargs: any) -> callable:
        result = func(*args, **kwargs)
        with open(str(Path(__file__).resolve().parent.parent) + os.sep + 'log.txt', 'a') as file:
            file.write(f'{datetime.now()} Command: {args[0]}, arguments: {args[1:]}, result{result}\n')

        return result

    return wrapper

