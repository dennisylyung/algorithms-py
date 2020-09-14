from typing import List


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


if __name__ == '__main__':
    array = MedianMaintainer()

    # array = list(range(50))
    # random.seed(0)
    # random.shuffle(array)
    # for i in array[1:]:

    medians = []

    with open('data/median.txt') as f:
        for i in f.readlines():
            array.put(int(i))
            medians.append(array.median())

    print(medians)
    print(len(medians))
    print(sum(medians) % 10000)
