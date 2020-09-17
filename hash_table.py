import math
import random
import unittest
from typing import Iterator, Iterable


def next_prime(num: int = 1):
    while True:
        if all(num % i != 0 for i in range(2, int(math.sqrt(num)) + 1)):
            return num
        num += 1


class HashSet:
    """
    An integer hash table using chaining. The Carter and Wegman integer hash function is used.
    """

    def __init__(self, elements: Iterable[int] = None, m: int = None, a: int = None, b: int = None, p: int = None):
        """
        Initialize a hash set. The set can be empty or include initial elements
        :param elements: optional elements to include initially.
        :param m: optional size of "buckets". defaults to 100, or twice the size of the elements
        :param a: optional a parameter for the hash function. defaults to a random value.
        :param b: optional b parameter for the hash function. defaults to a random value.
        :param p: optional p parameter for the hash function. defaults to a prime number larger than m.
        """
        if not m and hasattr(elements, '__len__'):
            m = len(elements) * 2
        elif not m:
            m = 100
        self.m = next_prime(m)
        self.a = a if a and a > 1 else random.randint(1, 65536)
        self.b = b if b else random.randint(0, 65536)
        self.p = p if p and p > m else next_prime(self.m + 1)
        self.data = [[] for _ in range(self.m)]
        if elements:
            self.update(elements)

    def hash(self, element: int) -> int:
        """
        hash the element
        :param element: the element
        :return: the hash value
        """
        return ((self.a * element + self.b) % self.p) % self.m

    def add(self, element) -> None:
        """
        add an element to the set
        :param element: the element
        :return: None
        """
        key = self.hash(element)
        for i in self.data[key]:
            if i == element:
                return
        self.data[key].append(element)
        return

    def remove(self, element) -> None:
        """
        Remove an element from the set. Removing a non-existent causes KeyError
        :param element: the element
        :return: None
        """
        key = self.hash(element)
        for i in range(len(self.data[key])):
            if self.data[key][i] == element:
                del self.data[key][i]
                return
        raise KeyError

    def update(self, elements: Iterable[int]) -> None:
        """
        add multiple elements to the set
        :param elements: the elements
        :return: None
        """
        for element in elements:
            self.add(element)
        return

    def __contains__(self, element) -> bool:
        key = self.hash(element)
        for i in self.data[key]:
            if i == element:
                return True
        return False

    def __len__(self) -> int:
        return sum([len(key) for key in self.data])

    def __iter__(self) -> Iterator[int]:
        for key in self.data:
            for element in key:
                yield element


def two_sum(numbers: HashSet, target: int, distinct=False) -> bool:
    """
    Check whether there exist a pair of numbers in the set that add up to the target.
    Using a hash set, this method runs in O(n) time
    :param numbers: the set of numbers
    :param target: the target sum
    :param distinct: whether only distinct pairs are considered.
    :return: True if there exists such a pair (or more), False otherwise.
    """
    for number in numbers:
        desired = target - number
        if distinct and desired == number:
            continue
        if desired in numbers:
            return True
    return False


class TestHashSet(unittest.TestCase):

    def test_init(self):
        items = HashSet([1, 1, 2, 3])
        self.assertEqual(len(items), 3)

    def test_contain(self):
        items = HashSet([3, 6, 9, 12, 15, 18])
        self.assertTrue(12 in items)
        self.assertFalse(13 in items)

    def test_delete(self):
        items = HashSet([3, 6, 9, 12, 15, 18])
        self.assertTrue(12 in items)
        items.remove(12)
        self.assertFalse(12 in items)


class TestTwoSum(unittest.TestCase):

    def test_positive(self):
        numbers = HashSet(range(-10, 10, 3))
        self.assertTrue(two_sum(numbers, 4))

    def test_negative(self):
        numbers = HashSet(range(-10, 10, 3))
        self.assertFalse(two_sum(numbers, 3))


if __name__ == '__main__':
    import time
    from multiprocessing import Pool
    from functools import partial

    with open('data/2sum.txt') as f:
        lines = f.readlines()

    numbers = HashSet([int(i) for i in lines if i])

    p = Pool(8)

    work = partial(two_sum, numbers)
    s = time.time()
    results = p.imap_unordered(work, range(-10000, 10000 + 1))
    print(sum(results))
    print(f'{len(list(range(-10000, 10000 + 1)))} 2-sums performed in {time.time() - s:.2f}s')
    # This takes O(kn) time
