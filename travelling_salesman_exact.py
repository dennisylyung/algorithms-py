import itertools
from typing import Sequence, Tuple, List

from scipy.spatial.distance import squareform, pdist


class EuclideanTravelingSalesman:
    """
    An travelling distance problem instance in Euclidean space.
    """

    def __init__(self, locations: Sequence[Tuple[float, float]]):
        """
        Initialize the travelling distance problem (TSP) instance with the {x. y} coordinates of locations
        :param locations: list of tuples of (x, y) coordinates
        """
        self.locations = list(locations)
        self.dist = squareform(pdist(locations))

    # def __dist(self, start: int, end: int) -> float:
    #     """
    #     Calculate the Euclidean distance between two points
    #     :param start: index of starting location
    #     :param end: index of ending location
    #     :return: distance
    #     """
    #     return math.dist(self.locations[start], self.locations[end])

    def solve(self) -> Tuple[List[int], float]:
        """
        Compute an exact solution of the travelling salesman problem using dynamic programming.
        It runs in O(n**2 * 2**n) time
        :return:
        """
        n = len(self.locations)  # assign location count to n for clarity

        subsets = [frozenset({location}) for location in range(n)]  # first iteration: sets of one location
        subproblem_values = {subset: [float('inf')] * n for subset in subsets}  # set all initial lengths to infinity
        subproblem_values[frozenset({0})][0] = 0  # the starting location (index 0) to itself has length 0

        # 2D array to store the paths of sub-problems
        subproblem_paths = {subset: [list() for _ in range(n)] for subset in subsets}
        subproblem_paths[frozenset({0})][0] = [0]  # the set {0} ending in [0] has a valid path [0]

        # loop through subsets of sizes from 2 to n
        # Since the start, 0, is in each set, the for loop is written as 1 to n-1
        for subset_size in range(1, n):
            # to save space, overwrite the previous sub-problem arrays in each iteration
            new_subproblem_values = {}
            new_subproblem_paths = {}

            # iterate over all combination of subset_size items plus location 0
            for subset_items in itertools.combinations(range(1, n), subset_size):

                subset = frozenset((0,) + subset_items)  # configure the subset
                new_subproblem_values[subset] = [float('inf')] * n  # initialize tour length array
                new_subproblem_paths[subset] = [list() for _ in range(n)]  # initialize tour path array
                for end in subset:
                    if end == 0:  # only sub-tours ending other than 0 are relevant
                        continue

                    # compute distance to end using each location in the subset as penultimate
                    sub_tours = []
                    for penultimate in subset:
                        if penultimate == end:
                            continue
                        full_length = subproblem_values[subset - {end}][penultimate] + self.dist[penultimate, end]
                        sub_tours.append((penultimate, full_length))

                    # save the minimum length and the respective path to the array
                    penultimate, full_length = min(sub_tours, key=lambda x: x[1])
                    new_subproblem_values[subset][end] = full_length
                    new_subproblem_paths[subset][end] = subproblem_paths[subset - {end}][penultimate] + [end]

            # overwrite the arrays
            subproblem_values = new_subproblem_values
            subproblem_paths = new_subproblem_paths

        # get the final arrays
        # in the last iteration, subset size equals n, so there is only one combination
        penultimate_tour_lengths = next(iter(subproblem_values.values()))
        penultimate_tour_paths = next(iter(subproblem_paths.values()))

        # compute full tour lengths using all possible penultimates
        tours = []
        for path, full_length in zip(penultimate_tour_paths[1:], penultimate_tour_lengths[1:]):  # skip 0
            # full tour length equals length to penultimate and distance from penultimate back to the start
            full_length = full_length + self.dist[path[-1], 0]
            tours.append((path + [0], full_length))

        shortest_path, shortest_length = min(tours, key=lambda x: x[1])
        return shortest_path, shortest_length


if __name__ == '__main__':
    import time

    with open('data/tsp.txt', mode='r') as f:
        lines = f.readlines()

    locations = []
    for line in lines[1:]:
        x, y = tuple(line.split(' '))
        locations.append((float(x), float(y)))

    s = time.time()
    tsp = EuclideanTravelingSalesman(locations)
    path, length = tsp.solve()
    print(f'shortest path {path} with length {length} found in {time.time() - s:.2f}s')
