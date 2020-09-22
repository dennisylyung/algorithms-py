from __future__ import annotations

from typing import Any


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

    def __repr__(self):
        return f'BinaryTreeNode <{self.value}>'
