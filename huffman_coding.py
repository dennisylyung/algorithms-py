import unittest
from queue import SimpleQueue
from typing import Sequence, Any, Iterable, Iterator

from binary_tree import BinaryTree
from heap import ValuedMinHeap


class HuffmanCoder:
    """
    A coder based on the Huffman coding algorithm.
    It compresses data in to variable length bits.
    """

    def __init__(self, weights: Sequence[float], keys: Sequence[Any] = None):
        """
        Initialize a coder on a set of alphabets with weights (frequencies)
        :param weights: weights or frequencies of the alphabets
        :param keys: the alphabets. Defaults to a range with the length of the weights.
        """
        # a minimum of 2 alphabets are required
        if len(weights) < 2:
            raise ValueError
        # validate alphabets or set the default
        if keys:
            assert len(keys) == len(weights)
        else:
            keys = range(len(weights))

        # use a heap to grow a binary tree bottom up in increasing order of the weights
        # the valued heap will keep track of both the weight for sorting, and the branches as values
        heap = ValuedMinHeap()
        for key, weight in zip(keys, weights):
            heap.put((weight, BinaryTree(key)))

        while len(heap) >= 2:
            weight1, tree1 = heap.get()
            weight2, tree2 = heap.get()
            heap.put((weight1 + weight2, BinaryTree(None, tree2, tree1)))

        # retrieve the final tree
        _, self.tree = heap.get()

        # search the tree to retrieve the key mapping
        # recursion can be used here, but a queue is used here to avoid max recursion error
        queue = SimpleQueue()
        queue.put((self.tree, ''))  # for simplicity, use a string to simulate the binary compressed data
        self.key_map = {}
        while not queue.empty():
            tree, prefix = queue.get()
            if tree.leave():
                self.key_map[tree.value] = prefix
                continue
            if tree.left_child:
                queue.put((tree.left_child, prefix + '0'))  # code left edges as 0
            if tree.right_child:
                queue.put((tree.right_child, prefix + '1'))  # code left edges as 1

    def compress(self, data: Iterable[Any]) -> str:
        """
        compress data to binary
        for simplicity a string will be returned
        :param data: data to be compressed
        :return: binary string of compressed bits
        """
        bits = ''
        for key in data:
            try:
                bits += self.key_map[key]
            except KeyError:
                raise KeyError(f'Unknown alphabet {key}')
        return bits

    def decompress(self, bits: str) -> Iterator[Any]:
        """
        decompress a binary string using the coder
        :param bits: compressed binary string
        :return: the original data
        """
        current_node = self.tree
        for bit in bits:
            if bit == '0':
                current_node = current_node.left_child
            elif bit == '1':
                current_node = current_node.right_child
            if not current_node:
                raise ValueError('Invalid sequence')
            if current_node.leave():
                yield current_node.value
                current_node = self.tree


class TestHuffmanCoding(unittest.TestCase):

    def test_coding(self):
        alphabets = ['A', 'B', 'C', 'D', 'E', 'F']
        weights = [0.1, 0.15, 0.05, 0.4, 0.05, 0.25]
        coder = HuffmanCoder(weights, alphabets)
        text = 'FEBCCFEADBAFCBE'
        bits = coder.compress(text)
        decompressed = ''.join(list(coder.decompress(bits)))
        self.assertEqual(text, decompressed)


if __name__ == '__main__':
    unittest.main(exit=False)

    with open(f'data/huffman.txt', mode='r') as f:
        data = f.readlines()
    weights = [int(line) for line in data[1:]]
    assert (len(weights) == int(data[0]))

    coder = HuffmanCoder(weights)
    print(f'Min length of codeword: {min([len(bits) for bits in coder.key_map.values()])}')
    print(f'Max length of codeword: {max([len(bits) for bits in coder.key_map.values()])}')
