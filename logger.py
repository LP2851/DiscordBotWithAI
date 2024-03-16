import functools
from datetime import datetime


def __log(message):
    print(f"[{datetime.now()}] :: {message}")

# region Decorators


def log(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        res = await func(*args, **kwargs)
        __log(f"[{func.__name__}] :: {str(res)}")
        return res
    return wrapper


def log_request(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        __log(f"[Request] {args[0]}")
        res = func(*args, **kwargs)
        __log(f"[Response] {res}")
        return res

    return wrapper

# endregion
