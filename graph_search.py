import unittest
from queue import LifoQueue, Queue
from typing import Dict, Tuple, List, Iterable, Iterator


class UndirectedGraph:

    def __init__(self, vertices: Dict[int, List[int]], edges: Dict[int, Tuple[int, int]]):
        """
        Initialize an adjacency lists representation of a undirected graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices at both ends
        """
        self.vertices = vertices
        self.edges = edges
        self.explored = None

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

    @classmethod
    def index_edges(cls, vertices: Iterable[int], edges: Iterable[Tuple[int, int]]):
        """
        Create undirected graph from lists of vertices and edges.
        :param vertices: list of vertices
        :param edges: list of edges represented by connecting vertices
        :return: an UndirectedGraph instance
        """
        vertices_dict = {k: [] for k in vertices}
        edges_dict = {}
        for i, edge in enumerate(edges):
            v1, v2 = edge
            vertices_dict[v1].append(i)
            if v1 != v2:
                vertices_dict[v2].append(i)
            edges_dict[i] = edge
        return cls(vertices_dict, edges_dict)

    def width_first_search(self, start_vertex: int, target_vertex: int = None) -> List[int]:
        """
        perform a width-first search on the graph.
        if a target vertex is provided, the shortest path is returned.
        Otherwise, all connected vertices are returned.
        :param start_vertex: the vertex to start the search
        :param target_vertex: the target vertex for shortest path. default to None
        :return:
            list of connected vertices if no target_vertex is provided.
            shortest path represented as list of vertices if a target_vertex is provided.
        """
        queue = Queue()
        queue.put([start_vertex])
        connected_vertices = []
        while not queue.empty():
            path = queue.get()
            vertex = path[0]
            if self.explored[vertex]:
                continue
            self.explored[vertex] = True
            # save connected vertex for full graph search
            connected_vertices.append(vertex)
            for edge in self.vertices[vertex]:
                v1, v2 = self.edges[edge]
                neighbor = v2 if v1 == vertex else v1
                if target_vertex and neighbor == target_vertex:
                    # return shortest path if target vertex is provided
                    return [neighbor] + path
                if not self.explored[neighbor]:
                    queue.put([neighbor] + path)
        return connected_vertices

    def shortest_path(self, start_vertex: int, target_vertex: int) -> List[int]:
        """
        Find the shortest path from the start_vertex to the target_vertex
        :param start_vertex: the vertex to start the search
        :param target_vertex: the target vertex for shortest path
        :return: shortest path represented as list of vertices if a target_vertex is provided
        """
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        return self.width_first_search(start_vertex, target_vertex)

    def connected_vertices(self, start_vertex: int) -> List[int]:
        """
        find all connected vertices from the start vertex
        :param start_vertex: the vertex to start the search
        :return: list of connected vertices
        """
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        return self.width_first_search(start_vertex)


class DirectedGraph:

    def __init__(self, vertices: Dict[int, List[int]], edges: Dict[int, Tuple[int, int]]):
        """
        Initialize an adjacency lists representation of a directed graph.
        :param vertices: map of vertices to list of indices of connecting edges
        :param edges: map of indices to list of tuples of vertices as (tail, head)
        """
        self.vertices = vertices
        self.edges = edges
        self.explored = None
        self.returned = None

    @classmethod
    def from_string(cls, data: str, sep=' '):
        """
        create a DirectedGraph instance with a line separated string representing undirected graphs,
        with each line a delimited list of indices.
        The first index refers to the vertice, and the later indices referring to the neighboring vertices
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
            edges += [(vertex, int(i)) for i in items[1:] if i != '' and int(i) > vertex]
        edges = {i: v for i, v in enumerate(edges)}
        for k, v in edges.items():
            for vertex in v:
                vertices[vertex].append(k)
        return cls(vertices, edges)

    @classmethod
    def index_edges(cls, vertices: Iterable[int], edges: Iterable[Tuple[int, int]]):
        """
        Create directed graph from lists of vertices and edges.
        :param vertices: list of vertices
        :param edges: list of edges represented by (tail, head)
        :return: a DirectedGraph instance
        """
        vertices_dict = {k: [] for k in vertices}
        edges_dict = {}
        for i, edge in enumerate(edges):
            tail, head = edge
            vertices_dict[tail].append(i)
            if head != tail:
                vertices_dict[head].append(i)
            edges_dict[i] = edge
        return cls(vertices_dict, edges_dict)

    def __depth_first_search_recursion(self, start_vertex: int, reverse=False) -> Iterator[int]:
        self.explored[start_vertex] = True
        for edge in self.vertices[start_vertex]:
            if not reverse:
                tail, head = self.edges[edge]
            else:
                head, tail = self.edges[edge]
            if tail == start_vertex and not self.explored[head]:
                yield from self.__depth_first_search_recursion(head, reverse)
        yield start_vertex

    def __depth_first_search_stack(self, start_vertex: int, reverse=False) -> Iterator[int]:
        stack = LifoQueue()
        stack.put(start_vertex)
        while not stack.empty():
            vertex = stack.get()
            if self.explored[vertex]:
                if not self.returned[vertex]:
                    yield vertex
                    self.returned[vertex] = True
                continue
            else:
                self.explored[vertex] = True
                stack.put(vertex)  # put vertex to be yielded when all downstream vertexes are searched
                for edge in self.vertices[vertex]:
                    if not reverse:
                        tail, head = self.edges[edge]
                    else:
                        head, tail = self.edges[edge]
                    if tail == vertex and not self.explored[head]:
                        stack.put(head)

    def depth_first_search(self, start_vertex: int, reverse=False, method='recursion') -> Iterator[int]:
        """
        Perform a depth-first search on the graph.
        Returns vertices in the order they are reached with no followable edge.
        :param start_vertex: the starting vertex for the search
        :param reverse: whether directed edges are treated in reverse. Defaults to False
        :param method: method for performing depth-first search, one of {'recursion', 'stack'}.
            For large graphs, the recursion will fail due to "maximum recursion reached" exception,
            so please use 'stack' instead. Defaults to 'recursion'
        :return: iterable of vertices
        """
        if method == 'recursion':
            yield from self.__depth_first_search_recursion(start_vertex, reverse)
        elif method == 'stack':
            yield from self.__depth_first_search_stack(start_vertex, reverse)
        else:
            raise ValueError(f'unknown method {method}. Available methods are "recursion" or "stack"')

    def find_scc(self, method=None) -> List[List[int]]:
        """
        Find strongly connected components (SCC) in the graph using Kosaraju's algorithm.
        :param method: method for performing depth-first search, one of {'recursion', 'stack'}.
            For large graphs, the recursion will fail due to "maximum recursion reached" exception,
            so please use 'stack' instead. Defaults to 'recursion'
        :return: list of SCCs represented by list of their vertices
        """

        # first pass
        sorted_vetices = []
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        self.returned = dict.fromkeys(list(self.vertices.keys()), False) if method == 'stack' else None

        for i, (vertex, _) in enumerate(self.vertices.items()):
            if not self.explored[vertex]:
                for target in self.depth_first_search(vertex, reverse=True, method=method):
                    sorted_vetices.append(target)
        sorted_vetices.reverse()
        print(f'SCC first pass finished')

        # second pass
        sccs = []
        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        self.returned = dict.fromkeys(list(self.vertices.keys()), False) if method == 'stack' else None

        for i, vertex in enumerate(sorted_vetices):
            if not self.explored[vertex]:
                sccs.append([i for i in self.depth_first_search(vertex, method=method)])
        print(f'SCC second pass finished')

        return sccs

    def topological_sort(self, method=None) -> List[int]:
        """
        Perform a topological sort on the graph.
        :param method: method for performing depth-first search, one of {'recursion', 'stack'}.
            For large graphs, the recursion will fail due to "maximum recursion reached" exception,
            so please use 'stack' instead. Defaults to 'recursion'
        :return: list of vertices sorted in ascending topoligical order
        """
        sorted_vertices = []

        self.explored = dict.fromkeys(list(self.vertices.keys()), False)
        self.returned = dict.fromkeys(list(self.vertices.keys()), False) if method == 'stack' else None

        while len(sorted_vertices) < len(self.vertices):
            start_vertex = next(k for k, v in self.explored.items() if not v)  # find first non-explored vertex
            sink_vertex = next(self.depth_first_search(start_vertex, method=method))
            sorted_vertices.append(sink_vertex)

            # use the explored flags to cut out sorted vertices
            self.explored = dict.fromkeys(list(self.vertices.keys()), False)
            self.explored.update(dict.fromkeys(sorted_vertices, True))

        sorted_vertices.reverse()
        return sorted_vertices


class TestUndirectedGraph(unittest.TestCase):

    def test_shortest_path(self):
        vertices = [1, 2, 3, 4, 5, 6, 7]
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 6), (5, 7), (6, 7)]
        graph = UndirectedGraph.index_edges(vertices=vertices, edges=edges)
        shortest_path = graph.shortest_path(3, 4)
        self.assertEqual(len(shortest_path), 4)

    def test_connected_vertices(self):
        vertices = [1, 2, 3, 4, 5, 6, 7]
        edges = [(1, 3), (2, 4), (2, 5), (4, 7), (5, 6), (5, 7), (6, 7)]
        graph = UndirectedGraph.index_edges(vertices=vertices, edges=edges)
        sub_graph = graph.connected_vertices(6)
        self.assertEqual(len(sub_graph), 5)


class TestDirectedGraph(unittest.TestCase):

    def test_sccs_recursion(self):
        graph = DirectedGraph.index_edges(
            vertices=range(1, 10),
            edges=[(1, 4), (2, 8), (3, 6), (4, 7), (5, 2), (6, 9), (7, 1), (8, 5), (8, 6), (9, 7), (9, 3)]
        )
        sccs = graph.find_scc(method='recursion')
        scc_sizes = [len(scc) for scc in sccs]
        self.assertEqual(scc_sizes, [3, 3, 3])

    def test_sccs_stack(self):
        graph = DirectedGraph.index_edges(
            vertices=range(1, 10),
            edges=[(1, 4), (2, 8), (3, 6), (4, 7), (5, 2), (6, 9), (7, 1), (8, 5), (8, 6), (9, 7), (9, 3)]
        )
        sccs = graph.find_scc(method='stack')
        scc_sizes = [len(scc) for scc in sccs]
        self.assertEqual(scc_sizes, [3, 3, 3])

    def test_topological_sort(self):
        vertices = [1, 2, 3, 4, 5, 6, 7]
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 7), (6, 7)]
        graph = DirectedGraph.index_edges(vertices=vertices, edges=edges)
        sorted_indices = graph.topological_sort(method='stack')
        for tail, head in edges:
            # assert no inversions
            self.assertTrue(sorted_indices.index(tail) < sorted_indices.index(head))


if __name__ == '__main__':
    import time

    print('loading file')
    vertices_set = set()
    edges = []
    with open(f'data/scc.txt', mode='r') as f:
        for line in f.readlines():
            vertices = line.split(' ')
            try:
                edges.append((int(vertices[0]), int(vertices[1])))
                vertices_set.add(int(vertices[0]))
                vertices_set.add(int(vertices[1]))
            except Exception as e:
                print(e)
                continue
    print(f'{len(vertices_set)} vertices, {len(edges)} edges loaded from file')

    graph = DirectedGraph.index_edges(vertices_set, edges)
    print('graph created from indexing edges')

    s = time.time()
    sccs = graph.find_scc(method='stack')
    print(f'SCCs found in {time.time() - s:.2f} seconds')

    scc_sizes = [len(scc) for scc in sccs]
    print(','.join([str(i) for i in sorted(scc_sizes, reverse=True)[:5]]))
