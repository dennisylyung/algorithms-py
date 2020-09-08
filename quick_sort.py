from typing import List


def quick_sort(arr: List[int], pivot_strategy='random', start=0, end=None) -> int:
    """
    sort the array with the quick sort algorithm in place. The count of comparisons is returned
    :param arr: the array to be sorted
    :param pivot_strategy: strategy of finding a pivot. One of {'first', 'last', 'median', 'random'}.
    :param start: starting index of array segment used in partitioning, defaults to 0
    :param end: starting index of array segment in partitioning, defaults to end of array
    defaults to 'random'
    :return: comparison count
    """
    if not end:
        end = len(arr) - 1

    if end - start <= 0:
        return 0

    if pivot_strategy == 'first':
        pivot_idx = start
    elif pivot_strategy == 'last':
        pivot_idx = end
    elif pivot_strategy == 'random':
        pivot_idx = random.randint(start, end)
    elif pivot_strategy == 'median':
        # "median-of-three" pivot rule
        middle = (end + start) // 2
        candidates = [start, middle, end]
        # bubble sort candidates to find median
        for i in [2, 1]:
            for j in range(i):
                if arr[candidates[j]] > arr[candidates[j + 1]]:
                    candidates[j], candidates[j + 1] = candidates[j + 1], candidates[j]
        pivot_idx = candidates[1]
    else:
        raise Exception(f'Unrecognized pivot strategy {pivot_strategy}')

    # swap first element with pivot
    arr[start], arr[pivot_idx] = arr[pivot_idx], arr[start]

    # partition around pivot
    pivot = arr[start]
    i = start + 1
    for j in range(start + 1, end + 1):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[start], arr[i - 1] = arr[i - 1], arr[start]

    # count comparisons for evaluation
    comparisons = end - start

    if i - 2 > start:
        # sort left partition
        comparisons += quick_sort(arr, pivot_strategy, start, i - 2)
    if end > start:
        # sort right partition
        comparisons += quick_sort(arr, pivot_strategy, i, end)

    # return count of comparisons for evaluation
    # since sort is performed in place, array is not returned
    return comparisons


if __name__ == '__main__':
    import random

    print(f'=====sorting randomly shuffled array=====')

    arr = list(range(100))
    random.shuffle(arr)

    for strategy in ['first', 'last', 'median', 'random']:
        arr_copy = arr.copy()
        com = quick_sort(arr_copy, strategy)
        assert arr_copy == sorted(arr)
        print(f'in {com} comparisons, sorted array using {strategy} pivot')

    print(f'=====sorting ascending array=====')

    arr = list(range(100))

    for strategy in ['first', 'last', 'median', 'random']:
        arr_copy = arr.copy()
        com = quick_sort(arr_copy, strategy)
        assert arr_copy == sorted(arr)
        print(f'in {com} comparisons, sorted array using {strategy} pivot')

    print(f'=====sorting long array=====')

    with open('data/quick_sort.txt', mode='r') as f:
        long_arr = f.readlines()

    long_arr = [int(i) for i in long_arr]

    for strategy in ['first', 'last', 'median', 'random']:
        arr_copy = long_arr.copy()
        com = quick_sort(arr_copy, strategy)
        assert arr_copy == sorted(long_arr)
        print(f'in {com} comparisons, sorted array using {strategy} pivot')
