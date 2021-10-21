from typing import List, Tuple
from unittest import TestCase


def find_cover(points: List[int], intervals: List[Tuple[float, float]]):
    points.sort()
    intervals.sort(key=lambda s: s[1], reverse=True)
    covered = [False] * len(points)
    selected_intervals = []

    for i, point in enumerate(points):
        if covered[i]:
            continue
        for (start, end) in intervals:
            # find cover with rightmost extension
            if start <= point <= end:
                selected_intervals.append((start, end))
                for j, point_to_cover in enumerate(points):
                    if start <= point_to_cover <= end:
                        covered[j] = True
                break
        else:
            raise Exception(f'No cover for point {point}')

    return selected_intervals


class TestSolution(TestCase):

    @staticmethod
    def assertValid(points, intervals, selected_intervals):
        for interval in selected_intervals:
            assert interval in intervals
        for point in points:
            for (start, end) in selected_intervals:
                if start <= point <= end:
                    break
            else:
                raise AssertionError

    def test_1(self):
        points = [0, 2, 6, 9, 11]
        intervals = [(0, 2), (2, 11), (6, 9), (9, 11)]
        selected_intervals = find_cover(points, intervals)
        self.assertEqual(2, len(selected_intervals))
        self.assertValid(points, intervals, selected_intervals)

    def test_2(self):
        points = [0, 2, 6, 9, 11, 12, 16, 18, 21]
        intervals = [(0, 6), (1, 7), (3, 9), (2, 11), (10, 16), (12, 17), (13, 19), (19, 25)]
        selected_intervals = find_cover(points, intervals)
        self.assertEqual(5, len(selected_intervals))
        self.assertValid(points, intervals, selected_intervals)
