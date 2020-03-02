
""" DO NOT modify the class name or the names of the provided functions

Please implement all functions that have pass
"""


class Stack(object):
    def __init__(self):
        self.stack = []

    def pop(self):
        return self.stack.pop(0)
        
    def top(self):
        return self.stack[0]

    def can_pop(self) -> bool:
        return len(self.stack) > 0

    def put(self, val):
        self.stack.insert(0, val)

    def to_array(self) -> list:
        return self.stack

