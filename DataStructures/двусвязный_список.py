import random


class Node:

    def __init__(self, data) -> None:
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:

    def __init__(self) -> None:
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if cur_node := self.head:
            # prev_node = None
            while cur_node.next:
                cur_node = cur_node.next
                # prev_node = cur_node
            cur_node.next = new_node
            cur_node.prev = cur_node
        else:
            self.head = new_node

    def insert(self, data):
        pass
