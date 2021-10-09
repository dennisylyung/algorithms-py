from __future__ import annotations

import unittest
from typing import Any, List


class BinaryTree:
    """
    A very simple binary tree
    """

    def __init__(self, value: Any = None, left_child: BinaryTree = None, right_child: BinaryTree = None):
        """
        Initialize a binary tree by its root.
        By default, a single node tree without value is created
        :param value: optional value of root node
        :param left_child: optional left child
        :param right_child: optional right child
        """
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    def leave(self):
        """
        Check if the tree (node) is a leave node.
        i.e. it has no children
        :return: whether it is a leave node
        """
        return self.left_child is None and self.right_child is None

    def traverse(self, order: str = 'preorder') -> List:
        """
        Return all values in the tree
        :param order: Traversal order, one of ('preorder', 'inorder', 'postorder')
        :return: list of values
        """
        traverse_left_child = self.left_child.traverse(order) if self.left_child else []
        traverse_right_child = self.right_child.traverse(order) if self.right_child else []
        if order == 'preorder':
            return [self.value] + traverse_left_child + traverse_right_child
        elif order == 'inorder':
            return traverse_left_child + [self.value] + traverse_right_child
        elif order == 'postorder':
            return traverse_left_child + traverse_right_child + [self.value]
        else:
            raise Exception(f'Unknown traversal order {order}')

    def __repr__(self):
        return f'BinaryTreeNode <{self.value}>'


class TestBinaryTree(unittest.TestCase):
    tree = BinaryTree('A',
                      BinaryTree('B',
                                 BinaryTree('D',
                                            BinaryTree('H'),
                                            BinaryTree('I')),
                                 BinaryTree('E',
                                            BinaryTree('J'))),
                      BinaryTree('C',
                                 BinaryTree('F'),
                                 BinaryTree('G')))

    def test_preorder_traversal(self):
        self.assertEqual(self.tree.traverse('preorder'),
                         ['A', 'B', 'D', 'H', 'I', 'E', 'J', 'C', 'F', 'G'])

    def test_inorder_traversal(self):
        self.assertEqual(self.tree.traverse('inorder'),
                         ['H', 'D', 'I', 'B', 'J', 'E', 'A', 'F', 'C', 'G'])

    def test_postorder_traversal(self):
        self.assertEqual(self.tree.traverse('postorder'),
                         ['H', 'I', 'D', 'J', 'E', 'B', 'F', 'G', 'C', 'A'])
