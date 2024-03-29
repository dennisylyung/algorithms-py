# Algorithms & Data structures in Python

A lot of classic algorithms and data structures, implemented in Python for my own learning. From the
Stanford [algorithm course](https://www.coursera.org/specializations/algorithms?) on Coursera, as well as many others
that I found fun to implement.

## Requirements

* Python 3.8+

## Getting started

Install dependencies

```shell script
pip install -r requirements.txt
```

## Algorithms
### Arithmetic
* Integer multiplication: [Karatsuba's algorithm](karatsuba_algorithm.py)
### Array
* Sort: [Merge Sort](merge_sort.py), [Quick Sort](quick_sort.py), [Insertion Sort](insertion_sort.py)
  , [Bubble Sort](bubble_sort.py)
* Search: [Linear Search](linear_search.py)
* Inversions: [Inversion Count](count_inversions.py)

### Graph

* Minimum cut: [Karger's algorithm](karger_min_cut.py)
* Graph search: [BFS](graph_search.py), [DFS](graph_search.py), [topological sort](graph_search.py)
* Strongly connected components: [Kosaraju's algorithm](graph_search.py)
* Shortest path: [BFS](graph_search.py), [Dijkstra's alogrithm](dijsktra_shortest_path.py),
  [Bellman-Ford algorithm](bellman_ford_algorithm.py), [Floyd-Warshall algorithm](floyd_warshall_algorithm.py)
* Minimum spanning tree: [Prim's algorithm](prim_mst.py), [Kruskal's algorithm](max_spacing_clustering.py)
* Clustering: [Maximum Spacing Clustering](max_spacing_clustering.py)
* Maximum weight independent set: [Dynamic programming](max_weight_independent_set.py)

### Optimisation

* Job scheduling: [Greedy algorithm](greedy_scheduling.py)
* Knapsack problem: [(Exact) Integer weight dynamic programming](knapsack.py)
* Set cover: [Greedy 1D interval cover algorithm](interval_set_cover.py)
* Travelling salesman problem: [(Exact) Dynamic programming](travelling_salesman_exact.py)
  , [(Heuristic) Nearest neighbour](travelling_salesman_nn.py)

### Others

* Lossless compression: [Huffman Coding](huffman_coding.py)
* 2-satisfiability (2-SAT) problem: [Strongly-connected-components algorithm](two_sat.py)

## Data Structures

* [Binary tree](binary_tree.py)
* [B+ tree](b_plus_tree.py)
* [Heap](heap.py)
* [Hash table](hash_table.py)
* [Union find](union_find.py)