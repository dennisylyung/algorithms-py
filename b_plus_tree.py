from math import ceil
from unittest import TestCase


class BPlusTree:
    """
    B+ Tree that supports search and insert.
    """

    def __init__(self, b):
        self.root = _BPlusTreeImpl(b)

    def __setitem__(self, key, value):
        self.root.insert(key, value)
        self.root = self.root.get_root()

    def __getitem__(self, key):
        return self.root.search(key)


class _BPlusTreeImpl:
    children = []

    def __init__(self, b, parent: '_BPlusTreeImpl' = None, children: list = None):
        self.b = b
        self.parent = parent
        self.children = [None] * self.node_len
        if children:
            self.children[:len(children)] = children

    @property
    def node_len(self):
        return self.b * 2 + 1

    def iter_nodes(self):
        for i in range(0, self.node_len, 2):
            yield i, self.children[i], self.children[i + 1] if i < self.node_len - 1 else None

    def index(self, value):
        i = 0
        while True:
            if i == self.node_len - 1:  # Greater than range
                return i
            elif self.children[i + 1] is None or value < self.children[i + 1]:
                return i
            elif value == self.children[i + 1]:
                return i + 1
            else:  # value > self.children[i+1]:
                i += 2
        pass

    def search(self, value):
        i = self.index(value)
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
                return target.search(value)
            else:
                raise KeyError

    def insert(self, value, obj):
        i = self.index(value)

        if i % 2 == 1 and type(self.children[i - 1]) is not _BPlusTreeImpl:  # odd index means an exact match
            self.children[i - 1] = obj  # replace value: this implementation does not support duplicate keys
        else:
            if self.is_leaf or type(obj) is _BPlusTreeImpl:
                if self.is_full:
                    self.split_and_insert(value, obj, i)
                else:
                    data_after = self.children[i:]
                    self.children[i + 2:i + len(data_after)] = data_after[:-2]
                    self.children[i:i + 2] = [obj, value]
            else:
                self.children[i + 1 if i % 2 else i].insert(value, obj)

    def get_root(self):
        if self.parent:
            return self.parent.get_root()
        else:
            return self

    @property
    def is_full(self):
        return self.children[-2] is not None

    def split_and_insert(self, value, obj, i):  # TODO: add insert item to signature, handle non leaf logic
        temp_nodes = self.children[:i] + [obj, value] + self.children[i:]
        mid_point = ceil((self.node_len + 2) / 2)
        if self.is_leaf:
            split_value = temp_nodes[mid_point + 1]
            new_node = _BPlusTreeImpl(self.b, None, temp_nodes[:mid_point] + [self])
            self.children = [None] * (self.node_len)
            self.children[:len(temp_nodes) - mid_point] = temp_nodes[mid_point:]
        else:
            split_value = temp_nodes[mid_point - 1]
            new_node = _BPlusTreeImpl(self.b, None, temp_nodes[:mid_point - 1])
            self.children = [None] * (self.node_len)
            self.children[:len(temp_nodes) - mid_point] = temp_nodes[mid_point:]
        if self.parent:
            self.parent.insert(split_value, new_node)
        else:
            parent = _BPlusTreeImpl(self.b, None, [new_node, split_value, self])
            new_node.parent = parent
            self.parent = parent

    @property
    def is_leaf(self):
        return type(self.children[2]) is not _BPlusTreeImpl


class BPlusTreeImplTest(TestCase):
    tree = _BPlusTreeImpl(b=4)

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
        self.assertEqual('data_2.5', self.tree.search(2.5))


class BPlusTreeUITest(TestCase):
    tree = BPlusTree(b=4)

    def setUp(self):
        for i in range(50):
            self.tree[i] = f'data_{i}'

    def test_get(self):
        for i in range(50, 7):
            self.assertEqual(f'data_{i}', self.tree[i])

    def test_insert(self):
        self.tree[100] = 'data_100'
        self.assertEqual('data_100', self.tree[100])
