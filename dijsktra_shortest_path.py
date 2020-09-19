import unittest
from typing import Dict, List, Tuple, Iterable, Union

from heap import ValuedMinHeap as MinHeap


class WeightedDirectedGraph:
    """
    A directed graph with edge weights.
    """

    def __init__(self, vertices: Dict[int, List[int]], edges: Dict[int, Tuple[int, int, float]]):
        """
        Initialize an adjacency lists representation of a weighted directed graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices as (tail, head, weight)
        """
        self.vertices = vertices
        self.edges = edges
        self.explored = None

    @classmethod
    def from_string(cls, data: str, sep=' '):
        """
        create a WeightedDirectedGraph instance with a line separated string representing directed graphs,
        with each line a delimited list of indices and weights.
        The first index refers to the vertice, and the later indices,weight pairs referring to the neighboring vertices
        :param data: the string representation
        :param sep: delimiter in rows. defaults to ' '
        :return: a DirectedGraph instance
        """
        lines = data.split('\n')
        vertices = {}
        edges = []
        for line in lines:
            if line == '':
                continue
            items = line.split(sep)
            vertex = int(items[0])
            vertices[vertex] = []
            for edge in items[1:]:
                if edge != '':
                    head, weight = edge.split(',')
                    edges.append((vertex, int(head), int(weight)))
        edges = {i: v for i, v in enumerate(edges)}
        for k, (v0, v1, w) in edges.items():
            for vertex in [v0, v1]:
                vertices[vertex].append(k)
        return cls(vertices, edges)

    @classmethod
    def index_edges(cls, vertices: Iterable[int], edges: Iterable[Tuple[int, int, int]]):
        """
        Create directed graph from lists of vertices and edges.
        :param vertices: list of vertices
        :param edges: list of edges represented by (tail, head, weight)
        :return: a WeightedDirectedGraph instance
        """
        vertices_dict = {k: [] for k in vertices}
        edges_dict = {}
        for i, edge in enumerate(edges):
            tail, head, weight = edge
            vertices_dict[tail].append(i)
            if head != tail:
                vertices_dict[head].append(i)
            edges_dict[i] = edge
        return cls(vertices_dict, edges_dict)

    def shortest_path(self, start_vertex: int, target_vertex: int = None) -> \
            Union[Dict[int, Tuple[List[int], int]], Tuple[List[int], int]]:
        """
        find the shortest path to vertices from a specific start.
        If no target is specified, a dictionary containing the path length and path
        for each of the vertices in the graph is returned.
        If a target is specified, both the path length and the path to the target is returned
        :param start_vertex: the starting vertex
        :param target_vertex: the target vertex. defaults to None
        :return:
            dictionary of {target vertex: (shortest path, path length)} if no target is specified
            tuple of (shortest path, path length) if a target is specified
        """
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        shortest_paths = dict.fromkeys(list(self.vertices.keys()), [])
        shortest_paths[start_vertex] = [start_vertex]
        shortest_path_length = dict.fromkeys(list(self.vertices.keys()), None)
        shortest_path_length[start_vertex] = 0
        heap = MinHeap.from_array([(0, start_vertex)])

        while heap:
            path_length, vertex = heap.get()
            self.explored[vertex] = True

            if target_vertex and target_vertex == vertex:
                return shortest_paths[vertex], shortest_path_length[vertex]

            frontier_vertices = {}

            for edge in self.vertices[vertex]:
                tail, head, weight = self.edges[edge]
                if tail == vertex and not self.explored[head]:
                    dijkstra_score = path_length + weight
                    if head not in frontier_vertices or dijkstra_score < frontier_vertices[head]:
                        frontier_vertices[head] = dijkstra_score

            for head, dijkstra_score in frontier_vertices.items():
                if head not in heap:
                    heap.put((dijkstra_score, head))
                    shortest_paths[head] = shortest_paths[vertex] + [head]
                    shortest_path_length[head] = dijkstra_score
                elif dijkstra_score < heap.get_key(head):
                    heap.update((dijkstra_score, head))
                    shortest_paths[head] = shortest_paths[vertex] + [head]
                    shortest_path_length[head] = dijkstra_score

        return {k: (path, shortest_path_length[k]) for k, path in shortest_paths.items()}


class TestWeightedDirectedGraph(unittest.TestCase):

    def test_shortest_path(self):
        vertices = [0, 1, 2, 3]
        edges = [(0, 1, 1), (0, 2, 4), (1, 2, 2), (1, 3, 6), (2, 3, 3)]
        graph = WeightedDirectedGraph.index_edges(vertices=vertices, edges=edges)
        paths = graph.shortest_path(0)
        self.assertEqual(list(paths.values()), [([0], 0), ([0, 1], 1), ([0, 1, 2], 3), ([0, 1, 2, 3], 6)])
        paths = graph.shortest_path(1, 3)
        self.assertEqual(paths, ([1, 2, 3], 5))


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/shortest_path.txt', mode='r') as f:
        data = f.read()
    graph = WeightedDirectedGraph.from_string(data, '\t')
    paths = graph.shortest_path(1)
    for target in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]:
        print(paths[target])
    print(','.join(str(paths[target][1]) for target in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]))
