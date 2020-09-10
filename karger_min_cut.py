import random
from typing import List, Dict, Tuple


class UndirectedGraph:

    def __init__(self, vertices: Dict[int, List[int]], edges: Dict[int, Tuple[int, int]]):
        """
        Initialize an adjacency lists representation of a undirected graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices at both ends
        """
        self.vertices = vertices
        self.edges = edges
        self.next_vertex = max(list(self.vertices.keys())) + 1

    @classmethod
    def from_string(cls, data: str, sep=' '):
        """
        create a undirectedGraph instance with a line separated string representing undirected graphs,
        with each line a delimited list of indices.
        The first index refers to the vertice, and the later indices referring to the neighboring vertices
        :param data: the string representation
        :param sep: delimiter in rows. defaults to ' '
        :return: an UndirectedGraph instancew
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
            edges += [(vertex, int(i)) for i in items[1:] if i != '' and int(i) > vertex]
        edges = {i: v for i, v in enumerate(edges)}
        for k, v in edges.items():
            for vertex in v:
                vertices[vertex].append(k)
        return cls(vertices, edges)

    def __contract_edge(self, edge: int):
        try:
            vertices = self.edges[edge]
        except KeyError:
            raise Exception(f'Graph has no edge {edge}')
        new_edges = set()
        for vertex in vertices:
            for connected_edge in self.vertices[vertex]:
                try:
                    v1, v2 = self.edges[connected_edge]
                except KeyError:
                    continue
                self.edges[connected_edge] = \
                    (self.next_vertex if v1 in vertices else v1, self.next_vertex if v2 in vertices else v2)
                if self.edges[connected_edge][0] == self.edges[connected_edge][1]:
                    del self.edges[connected_edge]
                else:
                    new_edges.add(connected_edge)
            del self.vertices[vertex]
        self.vertices[self.next_vertex] = list(new_edges)
        self.next_vertex += 1

    def karger_min_cut(self) -> List[Tuple[int, int]]:
        """
        estimate a min cut solution by iteratively cutting random edges
        :return: list of edges representing the edges to be cut
        """

        contraction = self.__class__(self.vertices.copy(), self.edges.copy())

        while True:
            edge_key = random.choice(list(contraction.edges.keys()))
            contraction.__contract_edge(edge_key)
            if len(contraction.vertices) == 2:
                return [self.edges[k] for k in contraction.edges.keys()]


def sample_contraction_cuts(data: str, sep=' '):
    import math
    graph = UndirectedGraph.from_string(data, sep=sep)
    print(f'Finding min cut for graph with {len(graph.vertices)} vertices')

    min_cuts = None
    best_cut = []
    trials = int(len(graph.vertices) ** 2 * math.log(len(graph.vertices)))
    for _ in range(trials):
        cuts = graph.karger_min_cut()
        if not min_cuts or len(cuts) < min_cuts:
            best_cut = cuts
            min_cuts = len(cuts)
    print(f'Min cut of {min_cuts} got in {trials} trials: {best_cut}')


if __name__ == '__main__':

    for i in range(5):
        with open(f'data/min_cut_samples/sample_0{i + 1}.txt', mode='r') as f:
            sample = f.read()
        sample_contraction_cuts(sample)

    with open(f'data/karger_min_cut.txt', mode='r') as f:
        data = f.read()
    sample_contraction_cuts(data, sep='\t')
