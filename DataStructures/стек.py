import random


class Stack:

    def __init__(self) -> None:
        self.stack = list()

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if self._is_empty():
            return None
        return self.stack.pop()

    def peek(self):
        if self._is_empty():
            return None
        return self.stack[-1]

    def _is_empty(self):
        return len(self.stack) == 0


stack = Stack()
rng = random.randint(20, 50)
for _ in range(rng):
    rnd_val = random.randint(20, 50)
    stack.push(rnd_val)

for _ in range(rng):
    value = stack.pop()
    print(value)
