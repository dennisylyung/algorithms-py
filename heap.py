import random
import unittest
from typing import List, Tuple, Any


class MinHeap:
    """
    A min heap supporting the basic create, put and get methods.
    """

    def __init__(self):
        """
        Initialize an empty heap
        """
        self.items = []

    @classmethod
    def from_array(cls, array: List[float]):
        """
        Initialize a heap from an array and sort the items
        :param array: array of items
        :return: a MinHeap instance
        """
        heap = cls()
        heap.items = array
        start_index = (len(array) - 2) // 2
        for i in range(start_index, -1, -1):
            heap.__bubble_down(i)
        return heap

    def __get_left_child(self, i):
        child = 2 * i + 1
        return child if child < len(self.items) else None

    def __get_right_child(self, i):
        child = 2 * i + 2
        return child if child < len(self.items) else None

    def __smallest_child(self, i):
        if not self.__get_left_child(i):
            return None
        if not self.__get_right_child(i):
            return self.__get_left_child(i)
        if self.items[self.__get_left_child(i)] < self.items[self.__get_right_child(i)]:
            return self.__get_left_child(i)
        else:
            return self.__get_right_child(i)

    def __get_parent(self, i):
        return (i - 1) // 2 if i > 0 else None

    def __swap(self, i, j):
        self.items[i], self.items[j] = self.items[j], self.items[i]

    def __bubble_up(self, i):
        while True:
            parent = self.__get_parent(i)
            if parent is not None and self.items[i] < self.items[parent]:
                self.__swap(i, parent)
                i = parent
            else:
                return

    def __bubble_down(self, i):
        while True:
            child = self.__smallest_child(i)
            if child and self.items[child] < self.items[i]:
                self.__swap(i, child)
                i = child
            else:
                return

    def put(self, item: float) -> None:
        """
        insert an item to the heap
        :param item: the item
        :return:
        """
        i = len(self.items)
        self.items.append(item)
        self.__bubble_up(i)

    def peek(self) -> float:
        """
        get the top item without removing it
        :return: the item
        """
        return self.items[0]

    def get(self) -> float:
        """
        get the top item without and remove it
        :return: the item
        """
        value = self.items[0]
        del self[0]
        return value

    def __delitem__(self, i) -> None:
        """
        delete an item by its index in the heap
        :param i: index of item
        :return:
        """
        self.items[i] = self.items[-1]
        del self.items[-1]
        self.__bubble_down(i)

    def __len__(self) -> int:
        """
        number if items in the heap
        :return: number if items
        """
        return len(self.items)

    def __bool__(self) -> bool:
        """
        whether the heap is non-empty
        :return: True if heap is non-empty, False if empty
        """
        return len(self.items) > 0


class TestMinHeap(unittest.TestCase):

    def assertHeap(self, heap: MinHeap):
        for i in range(len(heap.items)):
            child0 = heap._MinHeap__get_left_child(i)
            if child0:
                self.assertTrue(heap.items[i] < heap.items[child0])
                child1 = heap._MinHeap__get_right_child(i)
                if child1:
                    self.assertTrue(heap.items[i] < heap.items[child1])

    def test_init(self):
        random.seed(0)
        data = list(range(10))
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        self.assertHeap(heap)

    def test_pop(self):
        random.seed(0)
        data = list(range(10))
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        root = heap.get()
        self.assertEqual(root, 0)
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 9)

    def test_insert(self):
        random.seed(0)
        data = list(range(10))
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        heap.put(3.5)
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 11)


class ValuedMinHeap:
    """
    A min heap supporting the basic create, put and get methods.
    Additionally, this implementation also carries the value of items beside their priorities.
    Updating the priority of items based on their value is supported in O(nlogn).
    """

    def __init__(self):
        """
        Initialize an empty heap
        """
        self.items = []
        self.value_map = {}

    @classmethod
    def from_array(cls, array: List[Tuple[float, Any]]):
        """
        Initialize a heap from an array and sort the items
        :param array: array of items represented as (priority, value)
        :return: a ValuedMinHeap instance
        """
        heap = cls()
        heap.items = array
        heap.value_map = {v: i for i, (_, v) in enumerate(array)}
        start_index = (len(array) - 2) // 2
        for i in range(start_index, -1, -1):
            heap.__bubble_down(i)
        return heap

    def __get_left_child(self, i):
        child = 2 * i + 1
        return child if child < len(self.items) else None

    def __get_right_child(self, i):
        child = 2 * i + 2
        return child if child < len(self.items) else None

    def __smallest_child(self, i):
        if not self.__get_left_child(i):
            return None
        if not self.__get_right_child(i):
            return self.__get_left_child(i)
        if self.items[self.__get_left_child(i)][0] < self.items[self.__get_right_child(i)][0]:
            return self.__get_left_child(i)
        else:
            return self.__get_right_child(i)

    def __get_parent(self, i):
        return (i - 1) // 2 if i > 0 else None

    def __swap(self, i, j):
        val_i = self.items[i][1]
        val_j = self.items[j][1]
        self.items[i], self.items[j] = self.items[j], self.items[i]
        self.value_map[val_i] = j
        self.value_map[val_j] = i

    def __bubble_up(self, i):
        while True:
            parent = self.__get_parent(i)
            if parent is not None and self.items[i][0] < self.items[parent][0]:
                self.__swap(i, parent)
                i = parent
            else:
                return

    def __bubble_down(self, i):
        while True:
            child = self.__smallest_child(i)
            if child is not None and self.items[child][0] < self.items[i][0]:
                self.__swap(i, child)
                i = child
            else:
                return

    def put(self, item: Tuple[float, Any]) -> None:
        """
        insert an item to the heap
        :param item: the item represented as (priority, value)
        :return:
        """
        i = len(self.items)
        self.items.append(item)
        self.value_map[item[1]] = i
        self.__bubble_up(i)

    def peek(self) -> Tuple[float, Any]:
        """
        get the top item without removing it
        :return: the item represented as (priority, value)
        """
        return self.items[0]

    def get(self) -> Tuple[float, Any]:
        """
        get the top item without and remove it
        :return: the item represented as (priority, value)
        """
        value = self.items[0]
        del self[0]
        return value

    def update(self, item: Tuple[float, Any]) -> None:
        """
        update the priority of an item
        :param item: the item represented as (priority, value)
        :return:
        """
        try:
            i = self.value_map[item[1]]
        except KeyError:
            raise Exception(f'item {item[1]} is not in heap')
        old_key = self.items[i][0]
        self.items[i] = item
        if item[0] > old_key:
            self.__bubble_down(i)
        elif item[0] < old_key:
            self.__bubble_up(i)

    def __delitem__(self, i) -> None:
        """
        delete an item by its index in the heap
        :param i: index of item
        :return:
        """
        value = self.items[i][1]
        self.items[i] = self.items[-1]
        self.value_map[self.items[i][1]] = i
        del self.items[-1]
        del self.value_map[value]
        self.__bubble_down(i)

    def delete_value(self, value):
        """
        delete an item by its value
        :param value: value of item
        :return:
        """
        try:
            i = self.value_map[value]
        except KeyError:
            raise Exception(f'item {value} is not in heap')
        del self[i]

    def get_key(self, value):
        """
        get the priority of an item
        :param value: value of item
        :return:
        """
        try:
            i = self.value_map[value]
        except KeyError:
            raise Exception(f'item {value} is not in heap')
        return self.items[i][0]

    def __len__(self) -> int:
        """
        number if items in the heap
        :return: number if items
        """
        return len(self.items)

    def __bool__(self) -> bool:
        """
        whether the heap is non-empty
        :return: True if heap is non-empty, False if empty
        """
        return len(self.items) > 0

    def __contains__(self, value):
        """
        whether a value is contained in the heap
        :param value: value of item
        :return: True if heap contains this value, False otherwise
        """
        return value in self.value_map


class TestValuedMinHeap(unittest.TestCase):

    def assertHeap(self, heap: ValuedMinHeap):
        for i in range(len(heap.items)):
            child0 = heap._ValuedMinHeap__get_left_child(i)
            if child0:
                self.assertTrue(heap.items[i] < heap.items[child0])
                child1 = heap._ValuedMinHeap__get_right_child(i)
                if child1:
                    self.assertTrue(heap.items[i] < heap.items[child1])

    def test_init(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = ValuedMinHeap.from_array(data)
        self.assertHeap(heap)

    def test_pop(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = ValuedMinHeap.from_array(data)
        root = heap.get()
        self.assertEqual(root, (0, 'value_0'))
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 9)

    def test_insert(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = ValuedMinHeap.from_array(data)
        heap.put((3.5, 'value_3.5'))
        _ = heap.value_map['value_3.5']
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 11)

    def test_update(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = ValuedMinHeap.from_array(data)
        heap.update((0.5, 'value_5'))
        self.assertHeap(heap)
        heap.update((20, 'value_5'))
        self.assertHeap(heap)

    def test_delete(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = ValuedMinHeap.from_array(data)
        heap.delete_value('value_5')
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 9)


class MedianMaintainer:

    def __init__(self):
        self.lower_heap = MinHeap()
        self.upper_heap = MinHeap()

    def put(self, i: float):
        if not self.lower_heap:
            self.lower_heap.put(-i)
        else:
            if i < self.median():
                self.lower_heap.put(-i)
                if len(self.lower_heap) > (len(self.upper_heap) + 1):
                    self.upper_heap.put(-self.lower_heap.get())
            else:
                self.upper_heap.put(i)
                if len(self.upper_heap) > len(self.lower_heap):
                    self.lower_heap.put(-self.upper_heap.get())

    def median(self):
        if self.lower_heap:
            return -self.lower_heap.peek()
        else:
            raise ValueError('array is empty!')


class TestMedianMaintainer(unittest.TestCase):

    def test(self):
        array = MedianMaintainer()
        numbers = [10, 18, 16, 14, 0, 17, 11, 2, 3, 9, 5, 7, 4, 19, 6, 15, 8, 1, 13, 12]
        medians = []
        for i in numbers:
            array.put(int(i))
            medians.append(array.median())
        self.assertEqual(medians, [10, 10, 16, 14, 14, 14, 14, 11, 11, 10, 10, 9, 9, 9, 9, 9, 9, 8, 9, 9])


if __name__ == '__main__':
    unittest.main(exit=False)

    array = MedianMaintainer()
    medians = []

    with open('data/median.txt') as f:
        for i in f.readlines():
            array.put(int(i))
            medians.append(array.median())

    print(medians)
    print(len(medians))
    print(sum(medians) % 10000)
