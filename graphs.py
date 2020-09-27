from typing import Dict, List, Tuple, Sequence


class WeightedDirectedGraph:
    """
    A directed graph with edge weights.
    """

    def __init__(self, vertices: List[List[int]], edges: List[Tuple[int, int, float]],
                 vertex_key_map: Dict = None, vertex_value_map: List = None):
        """
        Initialize an adjacency lists representation of a weighted directed graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices as (tail, head, weight)
        """
        self.vertices = vertices
        self.edges = edges
        self.vertex_key_map = vertex_key_map if vertex_key_map else {}
        self.vertex_value_map = vertex_value_map if vertex_value_map else {}
        self.explored = None

    @classmethod
    def from_string(cls, data: str, sep=(' ', ' ')):
        """
        create a WeightedDirectedGraph instance with a line separated string representing directed graphs,
        with each line a delimited list of indices and weights.
        The first index refers to the vertex, and the later indices,weight pairs referring to the neighboring vertices
        :param data: the string representation
        :param sep: delimiter in rows. defaults to ' '
        :return: a DirectedGraph instance
        """
        lines = data.split('\n')
        vertices = []
        edges = []
        vertex_map = []

        # get an index for the vertex
        def index(v):
            try:
                return vertex_map.index(v)
            except ValueError:
                index = len(vertex_map)
                vertex_map.append(v)
                vertices.append(list())
                return index

        for line in lines:
            if line == '':
                continue
            items = line.split(sep[0], 1)
            vertex = index(int(items[0]))
            for edge in items[1:]:
                if edge != '':
                    head, weight = edge.split(sep[1])
                    edges.append((vertex, index(int(head)), int(weight)))
        for i, (v0, v1, w) in enumerate(edges):
            for vertex in [v0, v1]:
                vertices[vertex].append(i)
        vertex_key_map = {key: i for i, key in enumerate(vertex_map)}
        vertex_value_map = vertex_map
        return cls(vertices, edges, vertex_key_map, vertex_value_map)

    @classmethod
    def index_edges(cls, vertices: Sequence[int], edges: Sequence[Tuple[int, int, int]]):
        """
        Create directed graph from lists of vertices and edges.
        :param vertices: list of vertices
        :param edges: list of edges represented by (tail, head, weight)
        :return: a WeightedDirectedGraph instance
        """
        vertex_key_map = {key: i for i, key in enumerate(vertices)}
        vertex_value_map = list(vertices)
        vertices = [list() for _ in vertices]
        indexed_edges = []
        for i, edge in enumerate(edges):
            tail, head, weight = edge
            tail = vertex_key_map[tail]
            head = vertex_key_map[head]
            vertices[tail].append(i)
            if head != tail:
                vertices[head].append(i)
            indexed_edges.append((tail, head, weight))
        return cls(vertices, indexed_edges, vertex_key_map, vertex_value_map)
