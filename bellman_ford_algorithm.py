import unittest
from typing import Any, Union, Tuple, List

from graphs import WeightedDirectedGraph


class Graph(WeightedDirectedGraph):
    """
    WeightedDirectedGraph with an shortest_paths method.
    """

    def shortest_path(self, source: Any, target: Any = None) -> \
            Union[Tuple[List[int], List[List]], Tuple[int, List]]:
        """
        find the shortest path to vertices from a specific start.
        If no target is specified, a list of path lengths to all destinations, and one with the paths are returned
        If a target is specified, both the path length and the path to the target is returned
        :param source: the source vertex
        :param target: the optional target vertex
        :return:
            tuple of (path lengths, shortest paths) if no target is specified
            tuple of (path length, shortest path) if a target is specified
        :raises ValueError: if negative cycles exist in the graph
        """

        # get the index of source and target
        source = self.vertex_key_map[source]

        n = len(self.vertices)  # number of vertices
        m = len(self.edges)

        # initialize sub-problem values
        subproblem_values = [float('inf')] * n
        shortest_paths = [list() for _ in range(n)]

        # base cases
        subproblem_values[source] = 0  # shortest path length to itself is 0
        shortest_paths[source] = [source]  # shortest path to itself is itself

        # 1 to m-1 edges for shortest path, one extra iteration to detect negative cycles
        for n_edges in range(1, m + 1):

            # initialize a temporary array to hold the new sub-problem values
            new_subproblem_values = [float('inf')] * n

            for destination in range(n):

                # compute the path length for each penultimate vertex to the destination
                penultimate_vertices = []
                for edge in self.vertices[destination]:
                    tail, head, weight = self.edges[edge]
                    if head == destination:
                        penultimate_vertices.append((tail, weight))
                lengths_with_n_edges = [(v, subproblem_values[v] + w) for v, w in penultimate_vertices]
                # get the shortest path to the destination using n_edges edges
                penultimate_vertex, min_length_with_n_edges = min(lengths_with_n_edges, key=lambda x: x[1])

                length_with_less_edges = subproblem_values[destination]

                # store the new path length
                new_subproblem_values[destination] = min(length_with_less_edges, min_length_with_n_edges)
                # store the new path
                if min_length_with_n_edges < length_with_less_edges:
                    if penultimate_vertex == source:
                        shortest_paths[destination] = [destination]
                    else:
                        shortest_paths[destination] = shortest_paths[penultimate_vertex] + [destination]

            if n_edges < m:
                # replace the obsolete path lengths with the new ones
                subproblem_values = new_subproblem_values
            else:
                # in the final iteration, check for negative cycles
                # Only if negative cycles exist the path lengths using m edges will differ from those using m-1 edges
                if subproblem_values != new_subproblem_values:
                    raise ValueError('Graph contains negative cycle')

        if not target:
            # return all path lengths and paths if no target is specified
            for i, path in enumerate(shortest_paths):  # return the vertex keys instead of indices
                for j, vertex in enumerate(path):
                    shortest_paths[i][j] = self.vertex_value_map[shortest_paths[i][j]]
            return subproblem_values, shortest_paths
        else:
            # return the shortest path length and the path itself if a target is specified
            target = self.vertex_key_map[target]
            # return the vertex keys instead of indices
            shortest_path = [self.vertex_value_map[v] for v in shortest_paths[target]]
            return subproblem_values[target], shortest_path


class TestShortestPath(unittest.TestCase):

    def test_shortest_path(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (1, 3, 4), (2, 4, 2), (3, 4, 3), (4, 1, -2)]
        graph = Graph.index_edges(vertices=vertices, edges=edges)
        value, path = graph.shortest_path(3, 2)
        self.assertEqual(value, 2)
        self.assertEqual(path, [4, 1, 2])

    def test_shortest_paths(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (1, 3, 4), (2, 4, 2), (3, 4, 3), (4, 1, -2)]
        graph = Graph.index_edges(vertices=vertices, edges=edges)
        values, paths = graph.shortest_path(3)
        self.assertEqual(values, [1, 2, 0, 3])
        self.assertEqual(paths, [[4, 1], [4, 1, 2], [3], [4]])

    def test_negative_cycle(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (1, 3, 4), (2, 4, 2), (3, 4, 3), (4, 1, -4)]
        graph = Graph.index_edges(vertices=vertices, edges=edges)
        with self.assertRaises(ValueError):
            graph.shortest_path(3)
