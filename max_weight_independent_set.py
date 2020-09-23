import unittest
from typing import Sequence, Tuple, Set


def maximum_weight_independent_set(path: Sequence[int]) -> Tuple[int, Set[int]]:
    """
    compute the maximum weight independent set of a path graph using dynamic programming
    :param path: a path graph represented by a list of vertex weights
    :return: (maximum total weight, set of vertex indices)
    """

    # initialize weights of sub-problems
    subset_weights = [0] * len(path)

    # initialize the weights of the first 2 sub-problems
    subset_weights[0] = path[0]
    subset_weights[1] = max(path[0], path[1])

    for i in range(2, len(path)):
        weight_if_i = subset_weights[i - 2] + path[i]  # weight if the ith vertex is included
        weight_if_not_i = subset_weights[i - 1]  # weight if the ith vertex is not included
        subset_weights[i] = max(weight_if_i, weight_if_not_i)

    # initialize a set to save the reconstructed set
    max_set = set()
    i = len(path) - 1

    # loop through the weights from right to left to reconstruct the set
    while i > 1:
        weight_if_i = subset_weights[i - 2] + path[i]
        weight_if_not_i = subset_weights[i - 1]

        if weight_if_i > weight_if_not_i:
            # the set including the i-th node has higher weight, so include the vertex
            max_set.add(i)
            i -= 2
        else:
            i -= 1

    # evaluate whether the first 2 vertices are included
    if i == 1:
        max_set.add(1)
    else:
        max_set.add(0)

    return subset_weights[-1], max_set


class TestMwis(unittest.TestCase):

    def test_mwis(self):
        path = [1, 2, 5, 6, 7, 4, 3]
        weight, max_set = maximum_weight_independent_set(path)
        self.assertEqual(max_set, {0, 2, 4, 6})
        self.assertEqual(weight, 16)


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/mwis.txt', mode='r') as f:
        data = f.readlines()
    path = [int(line) for line in data[1:]]
    assert (len(path) == int(data[0]))

    weight, max_set = maximum_weight_independent_set(path)
    print(f'maximum weight independent set: {max_set} of weight {weight}')
