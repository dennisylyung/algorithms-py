import unittest
from typing import Tuple

import numpy as np

from graphs import WeightedDirectedGraph


class Graph(WeightedDirectedGraph):
    """
    WeightedDirectedGraph with an all_pairs_shortest_paths method.
    """

    def all_pairs_shortest_paths(self, return_paths=True) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute the shortest paths for all pairs of vertices in the graph using the Floyd-Warshall algorithm.
        Both the path lengths and paths are returned.
        :return: path length matrix, path matrix
        :raises ValueError: if negative cycles exist in the graph
        """
        n = len(self.vertices)  # number of vertices
        # For a memory efficient computation, store only the values for the previous k value
        subproblem_values = np.full((n, n), np.inf)
        if return_paths:
            latest_internal_vertex = np.full((n, n), np.NaN)

        # set length to selves to 0
        np.fill_diagonal(subproblem_values[:, :], 0)
        # set length of directly connected nodes to edge weight
        tails, heads, weights = tuple(map(list, zip(*self.edges)))  # unnest edges into lists of tails, heads, weights
        subproblem_values[tails, heads] = weights

        for nodes_considered in range(1, n + 1):  # add internal node into consideration incrementally
            k = nodes_considered - 1
            # vectorized version to compute values for all source-destination pairs
            # compute path length with or without the k-th internal node
            lengths_without_k = subproblem_values[:, :]
            lengths_with_k = np.repeat(subproblem_values[:, k][:, np.newaxis], n, axis=1) + \
                             np.repeat(subproblem_values[k, :][np.newaxis, :], n, axis=0)

            # record the shortest path length from source to destination using first k internal nodes
            subproblem_values = np.minimum(lengths_without_k, lengths_with_k)
            # record k as the latest internal node between source and destination
            if return_paths:
                latest_internal_vertex[lengths_with_k < lengths_without_k] = k
            # # for reference this is the non-vectorized version
            # for source in range(n):
            #     for destination in range(n):
            #         # compute path length with or without the k-th internal node
            #         length_without_k = subproblem_values[source, destination]
            #         length_with_k = subproblem_values[source, k] + subproblem_values[k, destination]
            #
            #         # record the shortest path length from source to destination using first k internal nodes
            #         subproblem_values[source, destination] = min(length_with_k, length_without_k)
            #
            #         # record k as the latest internal node between source and destination
            #         if return_paths and length_with_k < length_without_k:
            #             latest_internal_vertex[source, destination] = k

            # Check for negative cycles by checking for negative values on the diagonals

            if subproblem_values.diagonal().min() < 0:
                raise ValueError('Graph contains negative cycle')

        if return_paths:

            # initialize the path matrix
            shortest_paths = np.empty((n, n), np.object)

            # method to recursively reconstruct the paths from the latest_internal_vertex matrix
            def reconstruct_path(i, j):
                k = latest_internal_vertex[i, j]
                if np.isnan(k):
                    return [j]  # no internal nodes between i and j means they are directly connected
                else:
                    return reconstruct_path(i, int(k)) + reconstruct_path(int(k), j)

            # reconstruct the shortest paths
            for source in range(n):
                for destination in range(n):
                    shortest_paths[source, destination] = reconstruct_path(source, destination)

            return subproblem_values, shortest_paths

        else:
            return subproblem_values


class TestAPSP(unittest.TestCase):

    def test_shortest_path(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (1, 3, 4), (2, 4, 2), (3, 4, 3), (4, 1, -2)]
        graph = Graph.index_edges(vertices=vertices, edges=edges)
        values, paths = graph.all_pairs_shortest_paths()
        expected = np.array([[0., 1., 4., 3.], [0., 0., 4., 2.], [1., 2., 0., 3.], [-2., -1., 2., 0.]])
        self.assertTrue((values == expected).all())

    def test_negative_cycle(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (1, 3, 4), (2, 4, 2), (3, 4, 3), (4, 1, -4)]
        graph = Graph.index_edges(vertices=vertices, edges=edges)
        with self.assertRaises(ValueError):
            graph.all_pairs_shortest_paths()


if __name__ == '__main__':
    import time

    unittest.main(exit=False)
    file = 'data/g_big.txt'
    with open(file, mode='r') as f:
        data = f.readlines()

    vertices, edges = tuple(data[0].split(' '))
    graph = Graph.from_string('\n'.join(data[1:]), (' ', ' '))
    assert len(graph.vertices) == int(vertices)
    assert len(graph.edges) == int(edges)
    print(f'loaded graph with {vertices} vertices and {edges} edges')
    try:
        s = time.time()
        values = graph.all_pairs_shortest_paths(return_paths=False)
        print(f'shortest path in {file}: {values.min()} (computed in {time.time() - s:.2f}s)')
    except ValueError as e:
        print(f'cannot compute shortest paths for {file}: {e}')

    # for file in ['data/g1.txt', 'data/g2.txt', 'data/g3.txt']:
    #     with open(file, mode='r') as f:
    #         data = f.readlines()
    #
    #     vertices, edges = tuple(data[0].split(' '))
    #     graph = Graph.from_string('\n'.join(data[1:]), (' ', ' '))
    #     assert len(graph.vertices) == int(vertices)
    #     assert len(graph.edges) == int(edges)
    #     try:
    #         s = time.time()
    #         values = graph.all_pairs_shortest_paths(return_paths=False)
    #         print(f'shortest path in {file}: {values.min()} (computed in {time.time()-s:.2f}s)')
    #     except ValueError as e:
    #         print(f'cannot compute shortest paths for {file}: {e}')
