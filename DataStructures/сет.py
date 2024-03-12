import random


class HashSet:

    def __init__(self) -> None:
        self.capacity = 10
        self.size = 0
        self.table = [None] * self.capacity

    def add(self, key):
        if self.contains(key):
            return False
        idx = self.hash_func(key)
        if self.table[idx] is None:
            self.table[idx] = []
        self.table[idx].append(key)
        self.size += 1
        if self.size >= self.capacity * 0.7:
            self.resize()

        return True

    def remove(self, key):
        idx = self.hash_func(key)
        if self.table[idx]:
            try:
                self.table[idx].remove(key)
                self.size -= 1
                return True
            except ValueError:
                return False
        return False

    def contains(self, key):
        idx = self.hash_func(key)
        return (arr := self.table[idx]) is not None and key in arr

    def hash_func(self, key):
        return hash(key) % self.capacity

    def resize(self):
        self.capacity *= 2
        self.size = 0
        old_table = self.table
        self.table = [None] * self.capacity
        for bucket in old_table:
            if bucket:
                for key in bucket:
                    self.add(key)


hash_set = HashSet()
rng = random.randint(20, 50)
for _ in range(rng):
    rnd_val = random.randint(20, 50)
    hash_set.add(rnd_val)
    rnd_val = random.randint(20, 50)
    hash_set.remove(rnd_val)
