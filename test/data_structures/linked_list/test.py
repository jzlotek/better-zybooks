import unittest
import random

from linkedlist import LinkedList, Node


class Tests(unittest.TestCase):
    def setUp(self):
        self.ll = LinkedList()

    def test_empty(self):
        self.assertIsNone(self.ll.get_head())
        self.assertIsNone(self.ll.get_tail())

    def test_Append(self):
        val1 = 100
        self.ll.append(val1)
        self.assertIsNotNone(self.ll.get_head())
        self.assertIsNotNone(self.ll.get_tail())
        self.assertEqual(self.ll.get_tail().value, val1)
        self.assertEqual(self.ll.get_head().value, val1)


    def test_Prepend(self):
        val1, val2 = 100, 101
        self.ll.append(val1)
        self.assertIsNotNone(self.ll.get_head())
        self.assertIsNotNone(self.ll.get_tail())
        self.assertEqual(self.ll.get_tail().value, val1)
        self.assertEqual(self.ll.get_head().value, val1)
        self.ll.prepend(val2)
        self.assertEqual(self.ll.get_head().value, val2)
        self.assertNotEqual(self.ll.get_head().value, val1)


    def test_Remove(self):
        REM_VAL = 150
        for x in range(100, 200):
            self.ll.append(x)

        self.assertNotEqual(self.ll.find(REM_VAL), -1)

        self.ll.remove(REM_VAL)
        self.assertEqual(self.ll.find(REM_VAL), -1)

        self.ll = LinkedList()
        self.ll.append(REM_VAL)
        for x in range(100, 200):
            self.ll.append(x)
        self.ll.append(REM_VAL)

        self.assertNotEqual(self.ll.find(REM_VAL), -1)

        self.ll.remove(REM_VAL)
        self.assertEqual(self.ll.find(REM_VAL), -1)
        self.assertNotEqual(self.ll.get_tail(), REM_VAL)

    def test_Find(self):
        for x in range(100, 200):
            self.ll.append(x)
        self.assertEqual(self.ll.find(100), 0)
        self.assertEqual(self.ll.find(99), -1)
        self.assertTrue(self.ll.find(199), 99)

    def test_To_Array(self):
        for x in range(100, 200):
            self.ll.append(x)
        self.assertEquals(self.ll.to_array(), list(range(100, 200)))


