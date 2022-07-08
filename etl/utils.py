from functools import wraps
from time import sleep

from logger import logger

from typing import Type


def backoff(no_raise_exceptions: list[Type[BaseException]],
            start_sleep_time: float = 0.1,
            factor: int = 2,
            border_sleep_time: float = 10) -> callable:
    """
    The decorator to re-execute a function after some time if an exception was raised.
    It uses a naive exponential increasing of the repeating time.

    Formula:
        t = start_sleep_time * factor^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time

    :param no_raise_exceptions: the list of exceptions that will not be raised
    :param start_sleep_time: the start time of the repeating
    :param factor: the multiplier to increase the delay time
    :param border_sleep_time: the max delay time
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time if start_sleep_time < border_sleep_time else border_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if e not in no_raise_exceptions:
                        raise e
                    logger.warning(f'An exception occurred. Next attempt in {sleep_time} seconds.\n{e}')
                    logger.debug(f'Exception:\n{e}\n{e.args}')
                    sleep(sleep_time)
                    sleep_time *= factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper
