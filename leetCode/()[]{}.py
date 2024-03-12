"""Если задана строка s, содержащая только символы '(', ')', '{', '}', '[' и ']',
определите, является ли эта строка допустимой.

Входная строка является допустимой, если:
- Открытые скобки должны быть закрыты скобками того же типа.
- Открытые скобки должны быть закрыты в правильном порядке.
- Каждая закрытая скобка имеет соответствующую открытую скобку того же типа.

Пример 1 s = «{}[]()»
out := true

Пример 2 s = «{}[](»
out := false
"""

import time
import functools


def funcname(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling: {func.__name__}()')
        funcres = func(*args, **kwargs)
        print(f'TRACE: result: {funcres}')
        return funcres
    return wrapper


def worktime(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func_res = func(*args, **kwargs)
        res_time = time.time() - start_time
        print(f'Время анализа: {res_time}')
        return func_res
    return wrapper


class Solution:

    @worktime
    @funcname
    def isValid(self, s: str) -> bool:

        if not s:
            return False

        brackets = {
            ')': '(',
            '}': '{',
            ']': '['
        }

        stack = []
        for symbol in s:
            if symbol in brackets.values():
                stack.append(symbol)
            elif res := brackets.get(symbol):
                if stack and stack.pop() != res:
                    return False

        return False if stack else True


@worktime
@funcname
def main():
    var_arr = ["", "()[]{}", "{}[](", "{[()]}", "{{}}(жопа){{}}"]

    for s in var_arr:
        print(f"'{s}': {Solution().isValid(s)}")


if __name__ == '__main__':
    main()
