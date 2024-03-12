import time
import functools


def worktime(func):
    # @functools.wraps
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        res_time = time.time() - start
        args_str = f'{args}' if args else ''
        kwargs = f'{kwargs}' if kwargs else ''
        print(f'exec time fumc "{func.__name__}( {args_str};  {kwargs})": {res_time}')
        return res

    return wrapper


# @worktime
def print_simple_values(max_value: int):
    cur_value = 1
    print('Sequence simple values:')
    max_in_row = 20
    cur_in_row = 0
    while max_value >= cur_value:
        primary_values = [2, 3, 5, 7]
        is_simple = True
        for pk in primary_values:
            if cur_value == pk:
                break
            if cur_value % pk == 0:
                is_simple = False
                break
        if is_simple:
            if max_in_row > cur_in_row:
                print(cur_value, end=', ')
                cur_in_row += 1
            else:
                print(cur_value)
                cur_in_row = 0

        cur_value += 1

# @worktime
def get_factorial(factorial_value: int):

    def _get_factorial(value):
        if value < 1:
            print('err value')
            return value

        if value == 1:
            return value
        fv = _get_factorial(value-1) * value
        return fv

    return _get_factorial(factorial_value)


def fibonachi(limit:int):
    cur_value = 1
    prev_value = 1
    print(cur_value, end=', ')
    while limit > cur_value:
        print(cur_value, end=', ')
        tmp = cur_value
        cur_value += prev_value
        prev_value = tmp




def main():
    # print_simple_values(max_value=10000)
    for idx in range(1,15):
        res = get_factorial(idx)
        print(f'factorial of {idx} is {res}')
    # fibonachi(100000)

main()
