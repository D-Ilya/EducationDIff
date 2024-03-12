import random


class Query:

    def __init__(self) -> None:
        self.query = list()

    def enquery(self, data):
        self.query.append(data)

    def dequery(self):
        if self._is_empty():
            return None
        return self.query.pop(0)

    def _is_empty(self):
        return len(self.query) == 0


query = Query()
rng = random.randint(20, 50)
for _ in range(rng):
    rnd_val = random.randint(20, 50)
    query.enquery(rnd_val)

for _ in range(rng):
    value = query.dequery()
    print(value)
