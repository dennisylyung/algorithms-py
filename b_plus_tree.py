from __future__ import annotations

from math import ceil, floor
from typing import TypeVar, Generic, Union, List, Generator, Tuple
from unittest import TestCase

K = TypeVar("K")
V = TypeVar("V")


class BPlusTree(Generic[K, V]):
    """
    B+ Tree that supports search and insert.
    Insert with:                tree[key] = value
    Get with:                   tree[key]
    Slice (inclusive) with:     tree[key1:key2]
    Delete with:                del tree[key]
    """

    def __init__(self, b: int):
        self.root: _BPlusTreeImpl[K, V] = _BPlusTreeImpl(b)

    def __setitem__(self, key: K, value: V) -> None:
        self.root.insert(key, value)
        self.root = self.root.get_root()

    def __getitem__(self, key: K) -> V:
        if isinstance(key, slice):
            if key.step:
                raise NotImplementedError('step in key slicing not supported')
            return self.root.get_range(key.start, key.stop)
        elif isinstance(key, int):
            return self.root.search(key)

    def __delitem__(self, key: K):
        self.root.delete(key)

    def __len__(self) -> int:
        return len(self.root)


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
    def is_underfull(self) -> bool:
        min_nodes = ceil(self.b / 2) * 2
        return self.parent is not None and self.children[min_nodes - 1] is None

    @property
    def is_single_child_parent(self) -> bool:
        return (
                self.parent is None and
                type(self.children[1]) is _BPlusTreeImpl and
                self.children[1] is None
        )

    @property
    def is_leaf(self) -> bool:
        return type(self.children[0]) is not _BPlusTreeImpl

    @property
    def num_keys(self) -> int:
        return sum([1 for i in range(1, self.node_len, 2) if self.children[i] is not None])

    def get_root(self) -> _BPlusTreeImpl[K, V]:
        if self.parent is not None:
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
            raise KeyError
        else:
            target = self.children[i + 1 if i % 2 else i]
            if target:
                return target.search(key)
            else:
                raise KeyError

    def get_range(self, start_key: Union[K, None], end_key: K) -> List[V]:
        if start_key is not None:
            i = self._index(start_key)
        else:
            i = 0
        if self.is_leaf:
            results = []
            if i % 2:  # odd index means an exact match
                target = self.children[i - 1]
                if type(target) is not _BPlusTreeImpl:
                    results.append(target)
                i += 1
            while self.children[i] is not None:
                target = self.children[i]
                if type(target) is _BPlusTreeImpl:
                    results += target.get_range(None, end_key)
                    break
                else:
                    if end_key < self.children[i + 1]:
                        break
                    results.append(target)
                i += 2
            return results
        else:
            return self.children[i + 1 if i % 2 else i].get_range(start_key, end_key)

    def insert(self, key: K, value: V) -> None:
        i = self._index(key)

        if i % 2 == 1 and type(self.children[i - 1]) is not _BPlusTreeImpl:  # odd index means an exact match
            self.children[i - 1] = value  # replace value: this implementation does not support duplicate keys
        else:
            if self.is_leaf or type(value) is _BPlusTreeImpl:
                if self.is_leaf:
                    resulting_children = self.children[:i] + [value, key] + self.children[i:]
                else:  # type(value) is _BPlusTreeImpl
                    resulting_children = self.children[:i + 1] + [key, value] + self.children[i + 1:]
                if self.is_full:
                    self._split_and_insert(resulting_children)
                else:
                    self.children = resulting_children[:-2]

            else:
                self.children[i + 1 if i % 2 else i].insert(key, value)

    def delete(self, key: K, delete_node=False) -> None:
        i = self._index(key)
        if not self.is_leaf and not delete_node:
            target = self.children[i + 1 if i % 2 else i]
            if target:
                target.delete(key)
            else:
                raise KeyError
        else:
            if i % 2 == 0:  # no exact match
                raise KeyError
            elif type(self.children[i - 1]) is _BPlusTreeImpl and not delete_node:
                raise KeyError
            else:
                self.children[i - 1:] = self.children[i + 1:] + [None, None]
                if self.is_single_child_parent:
                    self.children = self.children[1].children
                elif self.is_underfull:
                    self.parent._merge_or_redistribute(self)

    def __len__(self) -> int:
        if self.is_leaf:
            non_empty_nodes = sum([1 for n in self.children if n is not None])
            return floor(non_empty_nodes / 2)
        else:
            return sum([len(self.children[i]) for i in range(0, self.node_len, 2) if self.children[i] is not None])

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

    def _split_and_insert(self, resulting_children: List[
        Union[None, K, V, _BPlusTreeImpl[K, V]]]) -> None:
        mid_point = ceil((self.node_len + 2) / 2)
        new_node = _BPlusTreeImpl(self.b, self.parent, resulting_children[mid_point:])
        self.children = [None] * self.node_len
        if new_node.is_leaf:
            split_value = resulting_children[mid_point + 1]
            self.children[:mid_point + 1] = resulting_children[:mid_point] + [new_node]
        else:
            split_value = resulting_children[mid_point - 1]
            self.children[:mid_point - 1] = resulting_children[:mid_point - 1]
        new_node._sync_children()
        self._sync_children()
        if self.parent is not None:
            self.parent.insert(split_value, new_node)
        else:
            parent = _BPlusTreeImpl(self.b, None, [self, split_value, new_node])
            new_node.parent = parent
            self.parent = parent
            pass

    def _merge_or_redistribute(self, underfull_node: _BPlusTreeImpl[K, V]) -> None:
        i = self.children.index(underfull_node)
        if i > 0:
            key_i, right_i = i - 1, i
            left_node = self.children[i - 2]
            merge_key = self.children[i - 1]
            right_node = underfull_node
        else:
            key_i, right_i = i + 1, i + 2
            left_node = underfull_node
            merge_key = self.children[i + 1]
            right_node = self.children[i + 2]

        left_size = left_node.num_keys * 2
        right_size = right_node.num_keys * 2 + 1
        if left_node.is_leaf:
            resulting_children = left_node.children[:left_size] + right_node.children[:right_size]
        else:
            resulting_children = left_node.children[:left_size + 1] + [merge_key] + right_node.children[:right_size]

        if len(resulting_children) <= self.node_len:
            left_node.children = resulting_children  # must use left node to maintain leaf pointers
            left_node._sync_children()
            self.children[right_i] = left_node
            self.delete(merge_key, delete_node=True)
        else:
            mid_point = ceil((self.node_len + 2) / 2)
            left_node.children = [None] * self.node_len
            right_node.children = [None] * self.node_len
            right_node.children[:mid_point] = resulting_children[mid_point:]
            if right_node.is_leaf:
                split_value = resulting_children[mid_point + 1]
                left_node[:mid_point + 1] = resulting_children[:mid_point] + [right_node]
            else:
                split_value = resulting_children[mid_point - 1]
                left_node[:mid_point - 1] = resulting_children[:mid_point - 1]
            left_node._sync_children()
            right_node._sync_children()
            self.children[key_i] = split_value

    def _sync_children(self) -> None:
        if self.is_leaf:
            return
        for node in self.children:
            if type(node) is _BPlusTreeImpl:
                node.parent = self


class BPlusTreeImplTest(TestCase):

    def setUp(self):
        self.tree: _BPlusTreeImpl[float, str] = _BPlusTreeImpl(b=4)
        children = []
        for i in range(1, 5):
            children += [f'data_{i}', i]
        children.append('next_pointer')
        self.tree.children = children

    def test_index(self):
        self.assertEqual(0, self.tree._index(-10))
        self.assertEqual(1, self.tree._index(1))
        self.assertEqual(4, self.tree._index(2.5))
        self.assertEqual(8, self.tree._index(10))

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

    def test_simple_delete(self):
        self.tree.delete(3)
        expected = [
            'data_1', 1,
            'data_2', 2,
            'data_4', 4,
            'next_pointer',
            None, None
        ]
        self.assertEqual(expected, self.tree.children)


class BPlusTreeUITest(TestCase):

    def setUp(self):
        self.tree = BPlusTree[int, str](b=4)
        for i in range(50):
            self.tree[i] = f'data_{i}'

    def test_len(self):
        self.assertEqual(50, len(self.tree))

    def test_get(self):
        for i in range(50, 7):
            self.assertEqual(f'data_{i}', self.tree[i])

    def test_slice(self):
        expected = ['data_13', 'data_14', 'data_15', 'data_16', 'data_17', 'data_18', 'data_19']
        self.assertEqual(expected, self.tree[12.5:19])

    def test_insert(self):
        self.tree[100] = 'data_100'
        self.assertEqual('data_100', self.tree[100])

    def test_delete(self):
        del self.tree[10]
        del self.tree[11]
        expected = ['data_7', 'data_8', 'data_9', 'data_12', 'data_13', 'data_14', 'data_15']
        self.assertEqual(expected, self.tree[7:15])
