from typing import Sequence, Tuple, List

import numpy as np
from scipy.spatial.distance import cdist


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

    def solve(self) -> Tuple[List[int], float]:
        """
        Compute an solution of the travelling salesman problem using nearest neighbour heuristic.
        It runs in O(n**2) time
        :return: Tour path in list of indices, length of tour
        """
        n = len(self.locations)  # assign location count to n for clarity

        tour_path = [0]
        tour_length = 0

        # go to the nearest unvisited location at each step
        for step in range(n - 1):
            # compute the required distances at each step to save memory
            dist = cdist([self.locations[tour_path[-1]]], self.locations)
            # set distance of visited locations to infinity
            mask = np.full(n, -np.inf)
            mask[tour_path] = np.inf
            dist = np.maximum(dist, mask)  # distance array with visited locations set to infinity
            tour_path.append(np.argmin(dist))  # get the next location
            tour_length += dist[0, tour_path[-1]]  # add the new edge to the length

        # return to the start
        tour_path.append(0)
        tour_length += cdist([self.locations[tour_path[-1]]], [self.locations[tour_path[-2]]])[0, 0]

        return tour_path, tour_length


if __name__ == '__main__':
    import time

    with open('data/nn.txt', mode='r') as f:
        lines = f.readlines()

    locations = []
    for line in lines[1:]:
        i, x, y = tuple(line.split(' '))
        locations.append((float(x), float(y)))

    tsp = EuclideanTravelingSalesman(locations)
    print(f'TSP instance with {len(tsp.locations)} locations loaded')
    s = time.time()
    path, length = tsp.solve()
    print(f'shortest path {path} with length {length} found in {time.time() - s:.2f}s')
