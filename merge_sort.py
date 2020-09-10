from typing import List


def merge_sort(arr: List[int]) -> List[int]:
    """
    Sort an integer array with merge sort
    :param arr: The array to be sorted
    :return: Sorted array
    """

    if len(arr) == 1:
        return arr

    midpoint = len(arr) // 2
    a0 = merge_sort(arr[:midpoint])
    a1 = merge_sort(arr[midpoint:])

    i, j = 0, 0

    output = []

    while True:
        if a0[i] < a1[j]:
            output.append(a0[i])
            i += 1
        else:
            output.append(a1[j])
            j += 1
        if i == len(a0):
            output += a1[j:]
            break
        if j == len(a1):
            output += a0[i:]
            break

    return output


if __name__ == '__main__':
    import random
    import time

    print(f'=====sorting randomly shuffled array=====')

    n = 10000
    arr = list(range(n))
    random.shuffle(arr)

    s = time.time()
    sorted_arr = merge_sort(arr)
    print(f'Merge sort on {n} elements in {(time.time() - s) * 1000:.2f} ms')
    assert sorted_arr == sorted(arr)

    trials = 100
    arrays = [list(range(n)) for _ in range(trials)]
    [random.shuffle(arr) for arr in arrays]

    print(f'=====benchmark merge sort=====')

    best_time = None
    worst_time = None
    for arr in arrays:

        s = time.time()
        sorted_arr = merge_sort(arr)
        run_time = time.time() - s

        if not best_time or run_time < best_time:
            best_time = run_time
        if not worst_time or run_time > worst_time:
            worst_time = run_time

    print(f'{trials} arrays of length {n} sorted with merge sort\n'
          f'best time: {best_time * 1000:.2f} ms\n'
          f'worst time: {worst_time * 1000:.2f} ms')

    print(f'=====benchmark quick sort=====')

    from quick_sort import quick_sort

    best_time = None
    worst_time = None
    for arr in arrays:

        s = time.time()
        quick_sort(arr)
        run_time = time.time() - s

        if not best_time or run_time < best_time:
            best_time = run_time
        if not worst_time or run_time > worst_time:
            worst_time = run_time

    print(f'{trials} arrays of length {n} sorted with quick sort\n'
          f'best time: {best_time * 1000:.2f} ms\n'
          f'worst time: {worst_time * 1000:.2f} ms')
