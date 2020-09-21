import logging
import sys
import unittest
from abc import ABC, abstractmethod
from typing import Any, Sequence


class UnionFind(ABC):

    @abstractmethod
    def __init__(self, elements: Sequence[Any]):
        pass

    @abstractmethod
    def find(self, element: Any) -> Any:
        """
        Find the partition representation of the specific element.
        Typically partitions are represented as one of their elements.
        :param element: the element to find
        :return: the partition representation
        """
        pass

    @abstractmethod
    def union(self, element_1: Any, element_2: Any) -> None:
        """
        Union the partitions containing the elements
        :param element_1: The first element
        :param element_2: The second element
        :return:
        """
        pass

    def neighbors(self, element_1: Any, element_2: Any) -> bool:
        """
        Return whether the two elements are within the same partition
        :param element_1: The first element
        :param element_2: The second element
        :return: The boolean value indicating if they are within the same partition
        """
        return self.find(element_1) == self.find(element_2)

    @abstractmethod
    def __len__(self) -> int:
        """
        the number of partitions in the union-find instance
        :return: the number of partitions
        """
        pass

    def __getitem__(self, item):
        """
        Find the partition representation of the specific element.
        Typically partitions are represented as one of their elements.
        :param item: the element to find
        :return: the partition representation
        """
        return self.find(item)


class EagerUnionFind(UnionFind):
    """
    Straightforward implementation of union find with the eager approach.
    This version performs find in O(1) and union in O(n)
    """

    def __init__(self, elements: Sequence[Any]):
        """
        Initialize a union-find with provided elements.
        :param elements: distinct elements of any type.
        """
        super().__init__(elements)
        self.index = {e: i for i, e in enumerate(elements)}  # map object values to indices
        self.partitions = list(range(len(elements)))  # initialize partitions of all elements to themselves
        self.sizes = [1] * len(elements)  # initialize all partition sizes to 1

    def find(self, element: Any) -> Any:
        return self.partitions[self.index[element]]

    def union(self, element_1: Any, element_2: Any) -> None:
        leader_1 = self.find(element_1)
        leader_2 = self.find(element_2)

        # to guarantee O(nlogn) time for unions, merge the smaller partition into the larger one
        if self.sizes[leader_1] < self.sizes[leader_2]:
            chg_from, chg_to = leader_1, leader_2
        else:
            chg_to, chg_from = leader_1, leader_2

        # update all items in the smaller partition to point to the larger partition
        for i in range(len(self.index)):
            if self.partitions[i] == chg_from:
                self.partitions[i] = chg_to

        # update the new partition size
        # Since the size of the smaller partition does not matter anymore, leave it as is
        self.sizes[chg_to] = self.sizes[leader_1] + self.sizes[leader_2]
        return

    def __len__(self) -> int:
        return len(set(self.partitions))


class LazyUnionFind(UnionFind):
    """
    Lazy union find with union by rank and path compaction.
    This version performs m of any operations in O(m*alpha(n)) time, where alpha is the inverse Ackermann function.
    """

    def __init__(self, elements: Sequence[Any]):
        """
        Initialize a union-find with provided elements.
        :param elements: distinct elements of any type.
        """
        super().__init__(elements)
        self.index = {e: i for i, e in enumerate(elements)}  # map object values to indices
        self.parents = list(range(len(elements)))  # initialize parents of all elements to themselves
        self.ranks = [0] * len(elements)  # initialize all union ranks to 0
        self.size = len(self.index)  # due to the tree structure, the partitions count need to be explicitly tracked

    def __get_root(self, index):
        """
        A subroutine to get find the root item, as well as performing path compaction
        :param index: index to current item
        :return: index of root
        """
        parent = self.parents[index]
        if parent == index:  # root items have parent of itself
            return parent  # return current index if it is a root
        else:
            root = self.__get_root(parent)
            self.parents[index] = root  # path compaction
            return root

    def find(self, element: Any) -> Any:
        index = self.index[element]
        root = self.__get_root(index)  # find root and perform path compaction recursively
        return root

    def union(self, element_1: Any, element_2: Any) -> None:
        root_1 = self.find(element_1)
        root_2 = self.find(element_2)
        if root_1 == root_2:
            return

        rank_1 = self.ranks[root_1]
        rank_2 = self.ranks[root_2]

        # to guarantee O(logn) time for find, merge the lower ranked root to the higher ranked root
        if rank_1 < rank_2:
            self.parents[root_1] = root_2
        elif rank_1 > rank_2:
            self.parents[root_2] = root_1
        else:  # rank_1 == rank_2
            self.parents[root_2] = root_1
            self.ranks[root_1] += 1  # rank of the new root need to have its rank added by 1 in this case
        self.size -= 1
        return

    def __len__(self) -> int:
        return self.size


class UnionFindTest(unittest.TestCase):

    def setUp(self) -> None:
        items = list(range(30))
        self.union_find: UnionFind = UnionFindImpl(items)

    def test_union_find(self):
        self.assertNotEqual(self.union_find[0], self.union_find[1])

    def test_union(self):
        self.assertNotEqual(self.union_find[0], self.union_find[1])
        for i in range(2, 24, 2):
            self.union_find.union(i, i + 2)
            self.assertEqual(self.union_find[2], self.union_find[i + 2])

    def test_neighbor(self):
        self.assertFalse(self.union_find.neighbors(2, 24))
        for i in range(2, 24, 2):
            self.union_find.union(i, i + 2)
            self.assertTrue(self.union_find.neighbors(2, i + 2))

    def test_length(self):
        self.assertEqual(len(self.union_find), 30)
        for i in range(2, 24, 2):
            self.union_find.union(i, i + 2)
        self.assertEqual(len(self.union_find), 19)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    for UnionFindImpl in UnionFind.__subclasses__():
        log = logging.getLogger("TestLog")
        log.debug(f'Testing sub-class {UnionFindImpl.__name__}')
        unittest.main(exit=False)
