"""
For testing, you should use two approaches:
    • unit tests (for all features)
    • property-based tests (for features with specific properties, such as monoid properties and
    conversation with built-in list).
"""

import unittest

from hypothesis import given
import hypothesis.strategies as st

from mutable import *


class TestMutableBTree(unittest.TestCase):

    def test_add(self):
        btree = BTree()
        btree.add(0)
        self.assertEqual(btree.to_list(), [0])
        btree.add(1)
        self.assertEqual(btree.to_list(), [1, 0])
        btree.add(2)
        self.assertEqual(btree.to_list(), [1, 0, 2])
        btree.add(3)
        self.assertEqual(btree.to_list(), [3, 1, 0, 2])
        btree.add(4)
        self.assertEqual(btree.to_list(), [3, 1, 4, 0, 2])

    def test_set_element(self):
        lst = [0, 1, 2]
        btree = BTree()
        btree.from_list(lst)
        btree.set_element(1, 3)
        self.assertEqual(btree.to_list(), [3, 1, 2])

    def test_parent(self):
        btree = BTree()
        for item in range(10):
            btree.add(item)
        self.assertIsNone(btree.parent(0))
        self.assertIsNotNone(btree.parent(1))

    def test_remove(self):
        btree = BTree()
        for i in range(10):
            btree.add(i)
        btree.remove(4)
        self.assertNotIn(btree.to_list(), [4])

    def test_size(self):
        btree = BTree()
        for i in range(10):
            btree.add(i)
        self.assertEqual(btree.size(), 10)

    def test_is_member(self):
        btree = BTree().from_list([0, 1, 2, 3, 4, 5])
        self.assertTrue(btree.is_member(2))
        self.assertTrue(btree.is_member(4))
        self.assertTrue(btree.is_member(1))

    def test_from_list(self):
        lst = [0, 1, 2]
        btree = BTree().from_list(lst)
        btree2 = BTree(BTNode(0, BTNode(1), BTNode(2)))
        self.assertEqual(btree.to_list(), btree2.to_list())

    def test_to_list(self):
        lst = [0, 1, 2, 3]
        btree = BTree()
        btree.from_list(lst)
        self.assertEqual(btree.to_list(), [3, 1, 0, 2])

    def test_filter(self):
        btree = BTree().from_list([0, 1, 'a', 2, 'b'])
        self.assertEqual(btree.filter(), [2, 1, 0])

    def test_map(self):
        lst = [0, 1, 2, 3, 4, 5]
        btree = BTree()
        btree.from_list(lst)
        btree.map(str)
        self.assertEqual(btree.to_list(), ["3", "1", "4", "0", "5", "2"])

        btree = BTree()
        btree.from_list(lst)
        btree.map(lambda x: x + 1)
        self.assertEqual(btree.to_list(), [4, 2, 5, 1, 6, 3])

    def test_reduce(self):
        # sum of empty btree
        btree = BTree()
        self.assertEqual(btree.reduce(lambda st, e: st + e, 0), 0)

        # sum of btree
        btree = BTree()
        btree.from_list([1, 2, 3])
        self.assertEqual(btree.reduce(lambda st, e: st + e, 0), 6)

        # size
        test_data = [
            [],
            [1, 2],
            [1, 2, 3]
        ]
        for e in test_data:
            btree = BTree()
        btree.from_list(e)
        self.assertEqual(btree.reduce(lambda st, _: st + 1, 0), btree.size())

    def test_next(self):
        lst = [0, 1, 2, 3, 4, 5]
        btree = BTree()
        btree.from_list(lst)

        iteration = iter(btree)

        self.assertIsNotNone(next(iteration))

    def test_concat(self):
        lst = [0, 1, 2]
        btree1 = BTree()
        btree1.from_list(lst)
        lst2 = [2, 4, 6]
        btree2 = BTree()
        btree2.from_list(lst2)

        btree = BTree()
        btree_root = btree.concat(btree1.root, btree2.root)
        self.assertEqual(BTree(btree_root).to_list(), [5, 2, 8])

    @given(st.lists(st.integers()))
    def test_from_list_to_list_equality(self, a):
        btree = BTree()
        btree.from_list(a)
        b = btree.to_list()
        self.assertCountEqual(a, b)

    @given(st.lists(st.integers()))
    def test_python_len_and_list_size_equality(self, a):
        btree = BTree()
        btree.from_list(a)
        self.assertEqual(btree.size(), len(a))

    @given(a=st.lists(st.integers()), b=st.lists(st.integers()), c=st.lists(st.integers()))
    def test_monoid_properties(self, a, b, c):
        """
        For all a, b and c in S, the equation a + b = b + a holds.
        For all a, b and c in S, the equation (a + b) + c = a + (b + c) holds.
        """
        btree1 = BTree()
        btree1.from_list(a)
        btree2 = BTree()
        btree2.from_list(b)
        btree3 = BTree()
        btree3.from_list(c)

        # the equation a + b = b + a
        btree_A = BTree(BTree().concat(btree1.root, btree2.root))
        btree_B = BTree(BTree().concat(btree2.root, btree1.root))

        self.assertEqual(btree_A.to_list(), btree_B.to_list())

        # (a + b) + c = a + (b + c)
        btree_A2 = BTree(BTree().concat(BTree().concat(btree1.root, btree2.root), btree3.root))
        # a+(b+c)
        btree_B2 = BTree(BTree().concat(btree1.root, BTree().concat(btree2.root, btree3.root)))
        self.assertEqual(btree_A2.to_list(), btree_B2.to_list())

    def test_iter(self):
        lst = [0, 1, 2, 3, 4, 5]
        btree = BTree()
        btree.from_list(lst)

        lst2 = []
        for item in btree.to_list():
            lst2.append(item)
        self.assertEqual(btree.to_list(), lst2)

        btree2 = BTree()
        iteration = iter(btree2)
        self.assertRaises(StopIteration, lambda: next(iteration))