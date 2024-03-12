import time
import functools


def time_exec(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        res_time = time.time() - start_time
        print(f'Время анализа: {res_time}')
        return res

    return wrapper


def func_name(func, with_args=False):
    @functools.wraps
    def wrapper(*args, **kwargs):
        print(f'func: {func.__name__}()')
        res = func(*args, **kwargs)
        if with_args:
            print(f'args: {args}' + f'\nkwargs: {kwargs}' if kwargs else '')
        return res

    return wrapper
