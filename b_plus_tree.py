from __future__ import annotations

from math import ceil
from typing import TypeVar, Generic, Union, List, Generator, Tuple
from unittest import TestCase

K = TypeVar("K")
V = TypeVar("V")


class BPlusTree(Generic[K, V]):
    """
    B+ Tree that supports search and insert.
    Insert with tree[key] = value
    Get with tree[key]
    """

    def __init__(self, b: int):
        self.root = _BPlusTreeImpl[K, V](b)

    def __setitem__(self, key: K, value: V) -> None:
        self.root.insert(key, value)
        self.root = self.root.get_root()

    def __getitem__(self, key: K) -> V:
        return self.root.search(key)


class _BPlusTreeImpl(Generic[K, V]):
    children: List[Union[None, K, V, _BPlusTreeImpl[K, V]]] = []

    def __init__(self, b: int, parent: _BPlusTreeImpl[K, V] = None, children: List = None):
        self.b = b
        self.parent = parent
        self.children = [None] * self.node_len
        if children:
            self.children[:len(children)] = children

    @property
    def node_len(self) -> int:
        return self.b * 2 + 1

    @property
    def is_full(self) -> bool:
        return self.children[-2] is not None

    @property
    def is_leaf(self) -> bool:
        return type(self.children[2]) is not _BPlusTreeImpl

    def get_root(self) -> _BPlusTreeImpl[K, V]:
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    def search(self, key: K) -> V:
        i = self._index(key)
        if self.is_leaf:
            if i % 2:  # odd index means an exact match
                target = self.children[i - 1]
                if type(target) is not _BPlusTreeImpl:
                    return target
            else:
                raise KeyError
        else:
            target = self.children[i + 1 if i % 2 else i]
            if target:
                return target.search(key)
            else:
                raise KeyError

    def insert(self, key: K, value: V) -> None:
        i = self._index(key)

        if i % 2 == 1 and type(self.children[i - 1]) is not _BPlusTreeImpl:  # odd index means an exact match
            self.children[i - 1] = value  # replace value: this implementation does not support duplicate keys
        else:
            if self.is_leaf or type(value) is _BPlusTreeImpl:
                if self.is_full:
                    self._split_and_insert(key, value, i)
                else:
                    data_after = self.children[i:]
                    self.children[i + 2:i + len(data_after)] = data_after[:-2]
                    self.children[i:i + 2] = [value, key]
            else:
                self.children[i + 1 if i % 2 else i].insert(key, value)

    def _iter_nodes(self) -> Generator[Tuple[int, Union[None, K, V, Generic[K, V]], Union[None, K, V, Generic[K, V]]]]:
        for i in range(0, self.node_len, 2):
            yield i, self.children[i], self.children[i + 1] if i < self.node_len - 1 else None

    def _index(self, key) -> int:
        i = 0
        while True:
            if i == self.node_len - 1:  # Greater than range
                return i
            elif self.children[i + 1] is None or key < self.children[i + 1]:
                return i
            elif key == self.children[i + 1]:
                return i + 1
            else:  # value > self.children[i+1]:
                i += 2
        pass

    def _split_and_insert(self, key: K, value: V, i: int) -> None:
        temp_nodes = self.children[:i] + [value, key] + self.children[i:]
        mid_point = ceil((self.node_len + 2) / 2)
        if self.is_leaf:
            split_value = temp_nodes[mid_point + 1]
            new_node = _BPlusTreeImpl(self.b, None, temp_nodes[:mid_point] + [self])
        else:
            split_value = temp_nodes[mid_point - 1]
            new_node = _BPlusTreeImpl(self.b, None, temp_nodes[:mid_point - 1])
        self.children = [None] * self.node_len
        self.children[:len(temp_nodes) - mid_point] = temp_nodes[mid_point:]
        if self.parent:
            self.parent.insert(split_value, new_node)
        else:
            parent = _BPlusTreeImpl(self.b, None, [new_node, split_value, self])
            new_node.parent = parent
            self.parent = parent


class BPlusTreeImplTest(TestCase):
    tree = _BPlusTreeImpl[int, str](b=4)

    def setUp(self):
        children = []
        for i in range(1, 5):
            children += [f'data_{i}', i]
        children.append('next_pointer')
        self.tree.children = children

    def test_index(self):
        self.assertEqual(0, self.tree.index(-10))
        self.assertEqual(1, self.tree.index(1))
        self.assertEqual(4, self.tree.index(2.5))
        self.assertEqual(8, self.tree.index(10))

    def test_search_single_layer(self):
        self.assertEqual('data_1', self.tree.search(1))
        with self.assertRaises(KeyError) as _:
            self.tree.search(-10)
        with self.assertRaises(KeyError) as _:
            self.tree.search(2.5)
        with self.assertRaises(KeyError) as _:
            self.tree.search(10)

    def test_insert_full(self):
        self.tree.insert(2.5, 'data_2.5')
        self.assertEqual('data_2.5', self.tree.get_root().search(2.5))


class BPlusTreeUITest(TestCase):
    tree = BPlusTree[int, str](b=4)

    def setUp(self):
        for i in range(50):
            self.tree[i] = f'data_{i}'

    def test_get(self):
        for i in range(50, 7):
            self.assertEqual(f'data_{i}', self.tree[i])

    def test_insert(self):
        self.tree[100] = 'data_100'
        self.assertEqual('data_100', self.tree[100])
