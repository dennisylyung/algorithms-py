import random
import unittest
from typing import Dict, List, Tuple, Any, Iterable, Union


class MinHeap:
    """
    A min heap supporting the basic create, put and get methods.
    Additionally, this implementation also carries the value of items beside their priorities.
    Updating the priority of items based on their value is supported in O(nlogn).
    """

    def __init__(self):
        """
        Initialize an empty heap
        """
        self.items = []
        self.value_map = {}

    @classmethod
    def from_array(cls, array: List[Tuple[float, Any]]):
        """
        Initialize a heap from an array and sort the items
        :param array: array of items represented as (priority, value)
        :return: a MinHeap instance
        """
        heap = cls()
        heap.items = array
        heap.value_map = {v: i for i, (_, v) in enumerate(array)}
        start_index = (len(array) - 2) // 2
        for i in range(start_index, -1, -1):
            heap.__bubble_down(i)
        return heap

    def __get_left_child(self, i):
        child = 2 * i + 1
        return child if child < len(self.items) else None

    def __get_right_child(self, i):
        child = 2 * i + 2
        return child if child < len(self.items) else None

    def __smallest_child(self, i):
        if not self.__get_left_child(i):
            return None
        if not self.__get_right_child(i):
            return self.__get_left_child(i)
        if self.items[self.__get_left_child(i)][0] < self.items[self.__get_right_child(i)][0]:
            return self.__get_left_child(i)
        else:
            return self.__get_right_child(i)

    def __get_parent(self, i):
        return (i - 1) // 2 if i > 0 else None

    def __swap(self, i, j):
        val_i = self.items[i][1]
        val_j = self.items[j][1]
        self.items[i], self.items[j] = self.items[j], self.items[i]
        self.value_map[val_i] = j
        self.value_map[val_j] = i

    def __bubble_up(self, i):
        while True:
            parent = self.__get_parent(i)
            if parent and self.items[i][0] < self.items[parent][0]:
                self.__swap(i, parent)
                i = parent
            else:
                return

    def __bubble_down(self, i):
        while True:
            child = self.__smallest_child(i)
            if child and self.items[child][0] < self.items[i][0]:
                self.__swap(i, child)
                i = child
            else:
                return

    def put(self, item: Tuple[float, Any]) -> None:
        """
        insert an item to the heap
        :param item: the item represented as (priority, value)
        :return:
        """
        i = len(self.items)
        self.items.append(item)
        self.value_map[item[1]] = i
        self.__bubble_up(i)

    def peek(self) -> Tuple[float, Any]:
        """
        get the top item without removing it
        :return: the item represented as (priority, value)
        """
        return self.items[0]

    def get(self) -> Tuple[float, Any]:
        """
        get the top item without and remove it
        :return: the item represented as (priority, value)
        """
        value = self.items[0]
        del self[0]
        return value

    def update(self, item: Tuple[float, Any]) -> None:
        """
        update the priority of an item
        :param item: the item represented as (priority, value)
        :return:
        """
        try:
            i = self.value_map[item[1]]
        except KeyError:
            raise Exception(f'item {item[1]} is not in heap')
        old_key = self.items[i][0]
        self.items[i] = item
        if item[0] > old_key:
            self.__bubble_down(i)
        elif item[0] < old_key:
            self.__bubble_up(i)

    def __delitem__(self, i) -> None:
        """
        delete an item by its index in the heap
        :param i: index of item
        :return:
        """
        value = self.items[i][1]
        self.items[i] = self.items[-1]
        self.value_map[self.items[i][1]] = i
        del self.items[-1]
        del self.value_map[value]
        self.__bubble_down(i)

    def delete_value(self, value):
        """
        delete an item by its value
        :param value: value of item
        :return:
        """
        try:
            i = self.value_map[value]
        except KeyError:
            raise Exception(f'item {value} is not in heap')
        del self[i]

    def get_key(self, value):
        """
        get the priority of an item
        :param value: value of item
        :return:
        """
        try:
            i = self.value_map[value]
        except KeyError:
            raise Exception(f'item {value} is not in heap')
        return self.items[i][0]

    def __len__(self) -> int:
        """
        number if items in the heap
        :return: number if items
        """
        return len(self.items)

    def __bool__(self) -> bool:
        """
        whether the heap is non-empty
        :return: True if heap is non-empty, False if empty
        """
        return len(self.items) > 0

    def __contains__(self, value):
        """
        whether a value is contained in the heap
        :param value: value of item
        :return: True if heap contains this value, False otherwise
        """
        return value in self.value_map


class TestMinHeap(unittest.TestCase):

    def assertHeap(self, heap: MinHeap):
        for i in range(len(heap.items)):
            child0 = heap._MinHeap__get_left_child(i)
            if child0:
                self.assertTrue(heap.items[i] < heap.items[child0])
                child1 = heap._MinHeap__get_right_child(i)
                if child1:
                    self.assertTrue(heap.items[i] < heap.items[child1])

    def test_init(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        self.assertHeap(heap)

    def test_pop(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        root = heap.get()
        self.assertEqual(root, (0, 'value_0'))
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 9)

    def test_insert(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        heap.put((3.5, 'value_3.5'))
        _ = heap.value_map['value_3.5']
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 11)

    def test_update(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        heap.update((0.5, 'value_5'))
        self.assertHeap(heap)
        heap.update((20, 'value_5'))
        self.assertHeap(heap)

    def test_delete(self):
        random.seed(0)
        data = [(i, f'value_{i}') for i in range(10)]
        random.shuffle(data)
        heap = MinHeap.from_array(data)
        heap.delete_value('value_5')
        self.assertHeap(heap)
        self.assertEqual(len(heap.items), 9)


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
        create a WeightedDirectedGraph instance with a line separated string representing undirected graphs,
        with each line a delimited list of indices and weights.
        The first index refers to the vertice, and the later indices,weight paris referring to the neighboring vertices
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
    with open(f'data/shortest_path.txt', mode='r') as f:
        data = f.read()
    graph = WeightedDirectedGraph.from_string(data, '\t')
    paths = graph.shortest_path(1)
    for target in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]:
        print(paths[target])
    print(','.join(str(paths[target][1]) for target in [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]))