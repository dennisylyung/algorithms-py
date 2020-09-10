from typing import List

from merge_sort import merge_sort


def linear_search(arr: List[int], order: int, pivot_strategy='random', start=0, end=None) -> int:
    """
    Search for the nth smallest element in array. Pivot partitioning is performed in place.
    :param arr: the array to be searched
    :param order: the nth element to return
    :param pivot_strategy: strategy of finding a pivot. One of {'random', 'median'}.
    :param start: starting index of array segment used in partitioning, defaults to 0
    :param end: starting index of array segment in partitioning, defaults to end of array
    :return: value of the nth element
    """

    if not end:
        end = len(arr) - 1

    if end - start <= 0:
        return arr[start]

    if pivot_strategy == 'random':
        pivot_idx = random.randint(start, end)
    elif pivot_strategy == 'median':
        # median of medians pivot
        arrays = [merge_sort(arr[i:min(i + 5, end)]) for i in range(start, end, 5)]  # break array into chunks of 5
        medians = [array[int(len(array) / 2)] for array in arrays]
        median_of_medians = linear_search(medians, int(len(medians) / 2))  # find median of medians recursively
        pivot_idx = arr.index(median_of_medians)
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

    if order == i - 1:
        return arr[i - 1]
    elif order < i - 1:
        return linear_search(arr, order, pivot_strategy, start, i - 2)
    else:
        return linear_search(arr, order, pivot_strategy, i, end)


if __name__ == '__main__':
    import random
    import time
    from quick_sort import quick_sort

    n = 10000

    arr = list(range(n))
    order = random.randrange(n)
    random.shuffle(arr)

    arr_copy = arr.copy()
    s = time.time()
    element = linear_search(arr_copy, order)
    print(f'Randomized linear search on {n} elements in {(time.time() - s) * 1000:.2f} ms')
    assert element == order

    arr_copy = arr.copy()
    s = time.time()
    element = linear_search(arr_copy, order, 'median')
    print(f'Deterministic linear search with on {n} elements in {(time.time() - s) * 1000:.2f} ms')
    assert element == order

    arr_copy = arr.copy()
    s = time.time()
    quick_sort(arr_copy)
    print(f'Quick sort on {n} elements in {(time.time() - s) * 1000:.2f} ms')
