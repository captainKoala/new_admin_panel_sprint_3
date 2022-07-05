from functools import wraps
import logging
from time import sleep


def backoff(start_sleep_time: float = 0.1, factor: int = 2, border_sleep_time: float = 10,
            logger: logging.Logger | None = None):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * factor^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param logger: логгер для вывода сообщений
    :return: результат выполнения функции
    """
    if not logger:
        logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    def func_wrapper(func, logger=logger):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time if start_sleep_time < border_sleep_time else border_sleep_time
            while True:
                try:
                    func(*args, **kwargs)
                    break
                except Exception as e:
                    logger.warning(f'An exception occurred. Next attempt in {sleep_time} seconds.\n{e}')
                    logger.debug(f'Exception:\n{e}')
                    sleep(sleep_time)
                    sleep_time *= factor
                    if sleep_time > border_sleep_time:
                        sleep_time = border_sleep_time
        return inner
    return func_wrapper
