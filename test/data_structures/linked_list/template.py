
""" DO NOT modify the class name or the names of the provided functions

Please implement all functions that have pass
"""


class Node(object):
    def __init__(self, value):
        self.value = value
        self.__next = None

    def get_next(self) -> Node:
        return self.next

    def set_next(self, node: Node):
        self.__next = node


class LinkedList(object):

    def __init__(self):
        """initialize LinkedList"""
        pass

    def append(self, value):
        """
        Appends value to end of list
        """
        pass

    def prepend(self, value):
        """
        Prepends value to start of list
        """
        pass

    def remove(self, key):
        """
        Removes all instances of key
        """
        pass

    def find(self, key) -> int:
        """
        Returns index of the first element in the list which
        matches the key
        Returns -1 on not found
        """
        pass

    def to_array(self) -> list:
        """
        Returns an array of all of the values in the Linked List
        """
        pass


"""
If you want to output anything for testing, print it in here
"""
if __name__ == "__main__":
    pass
