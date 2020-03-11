
""" DO NOT modify the class name or the names of the provided functions

Please implement all functions that have pass
"""


class Node(object):
    def __init__(self, value):
        self.value = value
        self.__next = None

    def get_next(self):
        return self.__next

    def set_next(self, node):
        self.__next = node


class LinkedList(object):

    def __init__(self):
        """initialize LinkedList"""
        self.head = None
        self.tail = None
    def get_head(self):
        return self.head
      
    def get_tail(self):
        return self.tail
        
    def append(self, value):
        """
        Appends value to end of list
        """
        n = Node(value)
        if self.head is None:
            self.head = n
            self.tail = n
        else:
            self.tail.set_next(n)
            self.tail = n

    def prepend(self, value):
        """
        Prepends value to start of list
        """
        n = Node(value)
        if self.head is None:
            self.head = n
            self.tail = n
        else:
            n.set_next(self.head)
            self.head = n

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
        arr = []
        curr = self.head
        while curr is not None:
            arr.append(curr.value)
            curr = curr.get_next()
        return arr


"""
If you want to output anything for testing, print it in here
"""
if __name__ == "__main__":
    pass
