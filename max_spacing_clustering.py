from __future__ import annotations

import unittest
from typing import Dict, List, Tuple, Iterable

from quick_sort import general_quick_sort as qsort
from union_find import LazyUnionFind as UnionFind


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
    def index_edges(cls, vertices: Iterable[int], edges: Iterable[Tuple[int, int, float]]):
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

    def clustering(self, k=4) -> float:
        """
        Perform maximum spacing clustering on the graph, stopping at k clusters
        :param k: number of clusters to stop at
        :return: the clyster spacing
        """
        # sort edges with a sef-made quick sort :D
        sorted_edges = list(self.edges.values()).copy()
        qsort(sorted_edges, lambda x: x[2])

        # initialize clusters
        clusters = UnionFind(list(self.vertices.keys()))

        # examine edges in ascending order of weight
        for edge in sorted_edges:
            v0, v1, weight = edge
            # edges within clusters are ignored
            if not clusters.neighbors(v0, v1):
                if len(clusters) == k:
                    # if the number of cluster is reached, return the next edge between clusters
                    return weight
                else:
                    # if the number of cluster is not reached, join clusters
                    clusters.union(v0, v1)
            continue

    def minimum_spanning_tree(self) -> WeightedUndirectedGraph:
        """
        Find the minimum spanning tree (MST) of the graph using Kruskal's algorithm
        :return: the minimum spanning tree as a WeightedUndirectedGraph
        """
        # sort edges with a sef-made quick sort :D
        sorted_edges = list(self.edges.values()).copy()
        qsort(sorted_edges, lambda x: x[2])

        # initialize clusters
        trees = UnionFind(list(self.vertices.keys()))

        mst_edges = []

        # examine edges in ascending order of weight
        for edge in sorted_edges:
            v0, v1, weight = edge
            if not trees.neighbors(v0, v1):
                trees.union(v0, v1)
                mst_edges.append(edge)
                if len(mst_edges) == len(self.vertices) - 1:
                    break
            continue

        # construct a WeightedUndirectedGraph to represent the minimum spanning tree
        mst = WeightedUndirectedGraph.index_edges(
            list(self.vertices.keys()),
            mst_edges)  # there is no edge saved for the starting vertex
        return mst


class TestWeightedDirectedGraph(unittest.TestCase):

    def test_mst(self):
        vertices = [1, 2, 3, 4]
        edges = [(1, 2, 1), (2, 4, 2), (3, 1, 4), (4, 3, 5), (4, 1, 3)]
        graph = WeightedUndirectedGraph.index_edges(vertices=vertices, edges=edges)
        mst = graph.minimum_spanning_tree()
        size = sum([weight for v0, v1, weight in mst.edges.values()])
        self.assertEqual(size, 7)


def custom_clustering():
    """
    Custom clustering routine to cluster based on hamming distance up to distance of 2
    :return:
    """

    # generate the candidate data
    def flip(text, positions):
        chars = list(text)
        for position in positions:
            if chars[position] == '0':
                chars[position] = '1'
            elif chars[position] == '1':
                chars[position] = '0'
        return ''.join(chars)

    with open('data/clustering_big.txt', 'r') as f:
        data = [line.replace(' ', '') for line in f.readlines()]

    clusters = UnionFind(data)

    # for each item, exhaust all the possible neighbors within distance of 2 and union clusters if found
    # there are 24 1st order and 276 2nd order neighbors for each item
    # hence this methods takes only O(n) comparisons, which is far superior to generating the n**2 distance matrix
    for idx, item in enumerate(data):

        # union 1st order neighbors if they exist
        for i in range(len(item)):
            try:
                clusters.union(item, flip(item, [i]))
            except KeyError:
                continue
        # union 2nd order neighbors if they exist
        for i in range(len(item)):
            for j in range(i + 1, len(item)):
                try:
                    clusters.union(item, flip(item, [i, j]))
                except KeyError:
                    continue

        if (idx + 1) % (len(data) // 20) == 0:
            print(f'finished checking for {idx + 1} items ({(idx + 1) * 100 / len(data)}%)')

    print(f'{len(clusters)} clusters within Hamming distance of 2')


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/hclust.txt', mode='r') as f:
        data = f.readlines()

    graph = WeightedUndirectedGraph.from_string('\n'.join(data), (' ', ' '))
    distance = graph.clustering(4)
    print(f'Cluster spacing: {distance}')

    # custom_clustering()
