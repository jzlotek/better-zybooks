import unittest
import random

from stack import Stack


class Tests(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_Put(self):
        for x in range(10):
            val = random.randint(499, 1000)
            self.stack.put(val)
            self.assertEqual(val, self.stack.top())

    def test_Pop(self):
        vals = [random.randint(499, 1000) for _ in range(100)]
        for val in vals:
            self.stack.put(val)

        for val in reversed(vals):
            popped_val = self.stack.pop()
            self.assertEqual(popped_val, val)

    def test_Can_Pop(self):
        self.assertFalse(self.stack.can_pop())
        self.stack.put(1)
        self.assertTrue(self.stack.can_pop())

    def test_To_Array(self):
        vals = [random.randint(499, 1000) for _ in range(100)]
        for val in vals:
            self.stack.put(val)

        self.assertEqual(list(reversed(vals)), self.stack.to_array())

    def test_Top(self):
        val = random.randint(1000, 9999)
        self.stack.put(val)
        self.assertEqual(val, self.stack.top())
