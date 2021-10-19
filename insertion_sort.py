import unittest
from typing import List


def insertion_sort(arr: List[int]):
    for i in range(1, len(arr)):
        candidate = arr[i]
        comparison = i - 1
        while comparison >= 0 and candidate < arr[comparison]:
            arr[comparison + 1] = arr[comparison]
            comparison -= 1
        arr[comparison + 1] = candidate


class Test(unittest.TestCase):

    def test_sort(self):
        arr = [4, 8, 1, 9, 0]
        insertion_sort(arr)
        self.assertEqual(arr, [0, 1, 4, 8, 9])
