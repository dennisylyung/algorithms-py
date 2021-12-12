import random
import time
import unittest


def bubble_sort(arr):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

    return arr


class Test(unittest.TestCase):

    def test_sort(self):
        arr = [4, 8, 1, 9, 0]
        bubble_sort(arr)
        self.assertEqual(arr, [0, 1, 4, 8, 9])


if __name__ == '__main__':
    print('benchmarking...')
    arr = list(range(1000))
    random.shuffle(arr)
    s = time.time()
    bubble_sort(arr)
    print(f'Sorted random array in {(time.time() - s) * 1000} milliseconds')
    arr = list(range(1000))
    s = time.time()
    bubble_sort(arr)
    print(f'Sorted ascending array in {(time.time() - s) * 1000} milliseconds')
    arr = list(range(1000))
    arr.reverse()
    s = time.time()
    bubble_sort(arr)
    print(f'Sorted descending array in {(time.time() - s) * 1000} milliseconds')
