"""
DO NOT modify the class name or the names of the prodided functions

Please implement all functions that have pass
"""


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None

    def get_next(self):
        return self.next

    def set_next(self, node):
        self.next = node


class LinkedList(object):

    def __init__(self):
        self.head = None
        self.tail = None

    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def append(self, value):
        node = Node(value)
        if self.tail is None:
            self.head = node
            self.tail = node
        else:
            self.get_tail().set_next(node)
            self.tail = node

    def prepend(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            node.set_next(self.head)
            self.head = node

    def remove(self, value):
        while self.head.value == value:
            self.head = self.head.get_next()
        curr = self.head
        nxt = curr.get_next()
        while nxt is not None:
            if nxt.value == value:
                curr.set_next(nxt.get_next())
            curr = nxt
            nxt = curr.get_next()

    def find(self, value):
        idx = -1
        count = 0
        curr = self.head
        while curr is not None:
            if curr.value == value:
                return count
            curr = curr.get_next()
            count += 1
        return idx

    def to_array(self):
        l = []
        curr = self.head
        while curr is not None:
            l.append(curr.value)
            curr = curr.get_next()
        return l
