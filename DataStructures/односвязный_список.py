
import random


class Node:

    def __init__(self, data) -> None:
        self.data = data
        self.next = None


class SinglyLinkedList:

    def __init__(self) -> None:
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if cur_node := self.head:
            while cur_node.next:
                cur_node = cur_node.next
            cur_node.next = new_node
        else:
            self.head = new_node
            return


sll = SinglyLinkedList()
for _ in range(random.randint(20, 50)):
    rnd_val = random.randint(20, 50)
    sll.append(rnd_val)

print()
