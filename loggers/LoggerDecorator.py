from datetime import datetime


def function_logger(func: callable) -> callable:
    def wrapper(*args: any, **kwargs: any) -> callable:
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()} Function: {func.__name__}, arguments: {args}\n')

        result = func(*args, **kwargs)
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()} Result: {result}\n')

        return result

    return wrapper


def command_logger(func: callable) -> callable:
    def wrapper(*args: any, **kwargs: any) -> callable:
        with open('log.txt', 'a') as file:
            file.write(f'{datetime.now()} Command: {args[0]}, arguments: {args[1:]}\n')

        return func(*args, **kwargs)

    return wrapper
