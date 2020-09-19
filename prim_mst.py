from __future__ import annotations

import unittest
from typing import Dict, List, Tuple, Iterable

from heap import ValuedMinHeap as MinHeap


class WeightedUndirectedGraph:
    """
    An undirected graph with edge weights.
    """

    def __init__(self, vertices: Dict[int, List[int]], edges: Dict[int, Tuple[int, int, float]]):
        """
        Initialize an adjacency lists representation of a weighted directed graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices as (v0, v1, weight)
        """
        self.vertices = vertices
        self.edges = edges
        self.explored = None

    @classmethod
    def from_string(cls, data: str, sep=(' ', ',')):
        """
        create a WeightedUndirectedGraph instance with a line separated string representing undirected graphs,
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
            items = line.split(sep[0], 1)
            vertex = int(items[0])
            vertices[vertex] = []
            for edge in items[1:]:
                if edge != '':
                    v1, weight = edge.split(sep[1])
                    edges.append((vertex, int(v1), int(weight)))
        edges = {i: v for i, v in enumerate(edges)}
        for k, (v0, v1, w) in edges.items():
            for vertex in [v0, v1]:
                try:
                    vertices[vertex].append(k)
                except KeyError:
                    vertices[vertex] = [k]
        return cls(vertices, edges)

    @classmethod
    def index_edges(cls, vertices: Iterable[int], edges: Iterable[Tuple[int, int, int]]):
        """
        Create directed graph from lists of vertices and edges.
        :param vertices: list of vertices
        :param edges: list of edges represented by (v0, v1, weight)
        :return: a WeightedUndirectedGraph instance
        """
        vertices_dict = {k: [] for k in vertices}
        edges_dict = {}
        for i, edge in enumerate(edges):
            v0, v1, weight = edge
            vertices_dict[v0].append(i)
            if v1 != v0:
                vertices_dict[v1].append(i)
            edges_dict[i] = edge
        return cls(vertices_dict, edges_dict)

    def minimum_spanning_tree(self) -> WeightedUndirectedGraph:
        """
        Find the minimum spanning tree (MST) of the graph using Prim's algorithm
        :return: the minimum spanning tree as a WeightedUndirectedGraph
        """
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        start_vertex = next(iter(self.vertices))  # start at the first vertex for simplicity
        heap = MinHeap.from_array([(0, start_vertex)])
        mst_edges = dict.fromkeys(list(self.vertices.keys()), None)  # store the edge connecting each vertex

        while heap:
            weight, vertex = heap.get()  # get the next vertex with the least edge weight
            self.explored[vertex] = True

            frontier_vertices = {}
            for edge in self.vertices[vertex]:
                v0, v1, weight = self.edges[edge]
                if self.explored[v0] and not self.explored[v1]:
                    target = v1
                elif self.explored[v1] and not self.explored[v0]:
                    target = v0
                else:
                    target = None
                if target and (target not in frontier_vertices or weight < frontier_vertices[target]):
                    frontier_vertices[target] = weight

            for target, weight in frontier_vertices.items():
                if target not in heap:
                    heap.put((weight, target))
                    mst_edges[target] = (vertex, target, weight)
                elif weight < heap.get_key(target):
                    heap.update((weight, target))
                    mst_edges[target] = (vertex, target, weight)

        # construct a WeightedUndirectedGraph to represent the minimum spanning tree
        mst = WeightedUndirectedGraph.index_edges(
            list(self.vertices.keys()),
            [edge for edge in mst_edges.values() if edge])  # there is no edge saved for the starting vertex
        return mst


class TestWeightedDirectedGraph(unittest.TestCase):

    def test_mst(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (2, 4, 2), (3, 1, 4), (4, 3, 5), (4, 1, 3)]
        graph = WeightedUndirectedGraph.index_edges(vertices=vertices, edges=edges)
        mst = graph.minimum_spanning_tree()
        size = sum([weight for v0, v1, weight in mst.edges.values()])
        self.assertEqual(size, 7)


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/mst.txt', mode='r') as f:
        data = f.readlines()

    n, m = data[0].split(' ')
    graph = WeightedUndirectedGraph.from_string('\n'.join(data[1:]), (' ', ' '))
    assert len(graph.vertices) == int(n)
    assert len(graph.edges) == int(m)
    mst = graph.minimum_spanning_tree()
    print(f'Minimum spanning tree size: {sum([weight for v0, v1, weight in mst.edges.values()])}')
