import logging
import time
import unittest
from queue import LifoQueue
from typing import Sequence, Tuple, Set

from quick_sort import general_quick_sort as qsort

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class KnapSack:

    def __init__(self, capacity: int, items: Sequence[Tuple[float, int]]):
        """
        Initialize a knapsack problem
        :param capacity: The total capacity of the knapsack
        :param items: Sequence of items represented as (value, volume)
        """
        self.capacity = capacity
        self.items = items
        self.subproblem_cache = {}

    def fit(self, method='iterative') -> Tuple[float, Set[int]]:
        """
        Find the knapsack load-out with the maximum value using dynamic programming.
        Optionally, a specific implementation can be picked.
        :param method: The implementation to use, one of ["iterative", "recursive", "stack"]. Defaults to 'iterative'.
            iterative: Iterate through all possible sub-problems with increasing room and item count.
                This brute force algorithm is the simplest.
            recursive: Start from the full problem, and recursively compute sub-problems with decreasing room
                and item count. This algorithm bypasses some sub-problems that are irrelevant to the final problem.
            stack: Essentially the recursive implementation, but implemented in a loop + stack pattern 
                that is more memory efficient in Python
        :return: (load-out value, load-out represented as the index of items)
        """
        if method == 'iterative':
            return self.__fit_iterative()
        elif method == 'recursive':
            return self.__fit_recursive()
        elif method == 'stack':
            return self.__fit_stack()
        else:
            raise ValueError(f'method {method} is not supported. supported are ["iterative", "recursive", "stack"]')

    def __fit_iterative(self) -> Tuple[float, Set[int]]:
        # initialize the 2-d array of sub-problem values
        subproblem_values = [[None] * (self.capacity + 1) for _ in range(len(self.items) + 1)]
        subproblem_values[0] = [0] * (self.capacity + 1)

        # iterate over increasing item count
        for n_items in range(1, len(self.items) + 1):
            # iterate over increasing capacity
            for room in range(self.capacity + 1):

                item_value, item_volume = self.items[n_items - 1]  # retrieve item to consider

                if item_volume <= room:
                    # value of this item with the optimized loadout for [room - item_volume]
                    value_if_i = subproblem_values[n_items - 1][room - item_volume] + item_value
                else:
                    # if the item cannot fit, it can not be picked. Set value to 0 so this won't be chosen
                    value_if_i = 0

                # value of load-out without current item
                value_if_not_i = subproblem_values[n_items - 1][room]

                # the higher of the two load-outs above
                subproblem_values[n_items][room] = max(value_if_i, value_if_not_i)

        # reconstruct the load-out items by looping over the sub-problem values
        loadout = set()
        while n_items > 0 and room > 0:

            item_value, item_volume = self.items[n_items - 1]  # retrieve item to consider

            # if the item cannot fit, ignore it
            if item_volume <= room:

                # calculate load-out values with and without this item
                value_if_i = subproblem_values[n_items - 1][room - item_volume] + item_value
                value_if_not_i = subproblem_values[n_items - 1][room]

                if value_if_i > value_if_not_i:
                    # this item should be included. Add it to the load-out, and remove its volume from remaining room.
                    room -= item_volume
                    loadout.add(n_items - 1)

            # Finished considering this item, move to the next
            n_items -= 1

        return subproblem_values[-1][-1], loadout

    def __subproblem_value(self, n_items: int, room: int) -> Tuple[int, Set[int]]:
        """
        Compute the value and load-out of a subproblem recursively
        :param n_items: the first n items to consider
        :param room: the remaining capacity
        :return: (load-out value, load-out represented as the index of items)
        """
        if (n_items, room) in self.subproblem_cache:
            # if this sub-problem is already solved, returns the cached solution
            return self.subproblem_cache[(n_items, room)]
        else:
            if n_items == 0 or room == 0:
                # if there are no room or no item to consider, return an empty load-out.
                self.subproblem_cache[(n_items, room)] = (0, set())  # cache the solution
                return 0, set()

            item_value, item_volume = self.items[n_items - 1]  # retrieve item to consider

            if item_volume <= room:
                # value of n_items with the optimized load-out for [room - item_volume]
                value_if_i, items_if_i = self.__subproblem_value(n_items - 1, room - item_volume)
                value_if_i += item_value
                items_if_i.add(n_items - 1)
            else:
                # if the item cannot fit, it can not be picked. Set value to 0 so this won't be chosen
                value_if_i = 0
                items_if_i = set()

            # value of load-out without current item
            value_if_not_i, items_if_not_i = self.__subproblem_value(n_items - 1, room)

            # cache and return the load-out with the higher value
            if value_if_i > value_if_not_i:
                self.subproblem_cache[(n_items, room)] = (value_if_i, items_if_i)
                return value_if_i, items_if_i
            else:
                self.subproblem_cache[(n_items, room)] = (value_if_not_i, items_if_not_i)
                return value_if_not_i, items_if_i

    def __fit_recursive(self):
        # initialize sub-problem value cache
        self.subproblem_cache = {}

        # compute the optimal load-out recursively
        value, items = self.__subproblem_value(len(self.items), self.capacity)

        return value, items

    def __fit_stack(self):
        # initialize sub-problem value cache, and the sub-problem to-do stack
        self.subproblem_cache = {}
        subproblem_stack = LifoQueue()

        # start with the full problem
        subproblem_stack.put((len(self.items), self.capacity))

        s = time.time()
        s0 = time.time()

        while not subproblem_stack.empty():
            # get the latest sub-problem
            n_items, room = subproblem_stack.get()

            if (n_items, room) in self.subproblem_cache:
                # skip if already computed
                continue
            else:
                if n_items == 0 or room == 0:
                    # if there are no room or no item to consider, cache an empty load-out.
                    self.subproblem_cache[(n_items, room)] = (0, set())  # cache the solution
                else:

                    item_value, item_volume = self.items[n_items - 1]  # retrieve item to consider

                    prerequisites = []  # if prerequisite sub-problems are not computed, add them to the to-do stack

                    if item_volume <= room:
                        subproblem = (n_items - 1, room - item_volume)
                        if subproblem in self.subproblem_cache:
                            # value of n_items with the optimized load-out for [room - item_volume]
                            value_if_i, items_if_i = self.subproblem_cache[subproblem]
                            value_if_i += item_value
                            items_if_i = items_if_i.copy()  # sets are mutable
                            items_if_i.add(n_items - 1)
                        else:
                            # this required sub-problem has no solution yet, do it later
                            prerequisites.append(subproblem)
                            value_if_i = None
                            items_if_i = None
                    else:
                        # if the item cannot fit, it can not be picked. Set value to 0 so this won't be chosen
                        value_if_i = 0
                        items_if_i = set()

                    subproblem = (n_items - 1, room)
                    if subproblem in self.subproblem_cache:
                        # value of load-out without current item
                        value_if_not_i, items_if_not_i = self.subproblem_cache[subproblem]
                    else:
                        # this required sub-problem has no solution yet, do it later
                        prerequisites.append(subproblem)
                        value_if_not_i = None
                        items_if_not_i = None

                    # compute the optimal solution if prerequisites are met
                    if value_if_i is not None and value_if_not_i is not None:
                        # cache the load-out with the higher value
                        if value_if_i > value_if_not_i:
                            self.subproblem_cache[(n_items, room)] = (value_if_i, items_if_i)
                        else:
                            self.subproblem_cache[(n_items, room)] = (value_if_not_i, items_if_not_i)
                    else:
                        # put the outer problem first so it is called after the prerequisites
                        subproblem_stack.put((n_items, room))
                        for subproblem in prerequisites:
                            # put the prerequisites to the stack
                            subproblem_stack.put(subproblem)

            if time.time() - s > 20:
                logger.info(
                    f'completed {len(self.subproblem_cache)} sub-problems in {time.time() - s0:.0f}s, {subproblem_stack.unfinished_tasks} in stack')
                s = time.time()

        # retrieve the solution from the caches
        value, items = self.subproblem_cache[(len(self.items), self.capacity)]

        return value, items


class TestKnapsack(unittest.TestCase):

    def test_knapsack(self):
        items = [
            (3, 4),
            (2, 3),
            (4, 2),
            (4, 3)
        ]

        knapsack = KnapSack(6, items)
        value, loadout = knapsack.fit()
        self.assertEqual(value, 8)
        self.assertEqual(loadout, {2, 3})

    def test_recursive_knapsack(self):
        items = [
            (3, 4),
            (2, 3),
            (4, 2),
            (4, 3)
        ]

        knapsack = KnapSack(6, items)
        value, loadout = knapsack.fit(method='recursive')
        self.assertEqual(value, 8)
        self.assertEqual(loadout, {2, 3})

    def test_stack_knapsack(self):
        items = [
            (3, 4),
            (2, 3),
            (4, 2),
            (4, 3)
        ]

        knapsack = KnapSack(6, items)
        value, loadout = knapsack.fit(method='stack')
        self.assertEqual(value, 8)
        self.assertEqual(loadout, {2, 3})


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/knapsack_big.txt', mode='r') as f:
        data = f.readlines()
    data = [tuple(line.split(' ', 2)) for line in data]
    data = [(int(v), int(w)) for v, w in data]
    assert (len(data) - 1 == int(data[0][1]))

    items = data[1:]
    qsort(items, lambda x: x[1])
    knapsack = KnapSack(data[0][0], items)
    value, loadout = knapsack.fit('stack')

    print(value)
    print(loadout)
