from typing import List


def count_inversions(arr: List[int]) -> (int, List[int]):
    """
    count inversions in an integer array recursively
    :param arr: an integer array
    :return: (number of inversions, sorted array)
    """
    n = len(arr)

    # return 0 inversions if arr contains a single integer
    if n == 1:
        return 0, arr

    # split array into halves and count inversions recursively
    m = int(n / 2)
    x_inv, x_sorted = count_inversions(arr[:m])
    y_inv, y_sorted = count_inversions(arr[m:])

    # count cross inversions in a merge sort
    i = 0
    j = 0
    cross_inv = 0
    sorted_arr = []
    while True:
        if x_sorted[i] <= y_sorted[j]:
            sorted_arr.append(x_sorted[i])
            i += 1
        else:
            sorted_arr.append(y_sorted[j])
            j += 1
            cross_inv += len(x_sorted) - i

        # if either x or y is exhausted, break the loop
        if i == len(x_sorted):
            sorted_arr += y_sorted[j:]
            break
        if j == len(y_sorted):
            sorted_arr += x_sorted[i:]
            break

    # number of inversions equals to inversions in both halves plus cross inversions
    return x_inv + y_inv + cross_inv, sorted_arr


if __name__ == '__main__':
    import random

    arr = list(range(10))
    random.shuffle(arr)

    inv, _ = count_inversions(arr)
    print(f'{inv} inversions in {arr}')

    with open('data/inv_array.txt', mode='r') as f:
        long_arr = f.readlines()

    long_arr = [int(i) for i in long_arr]

    inv, _ = count_inversions(long_arr)
    print(f'{inv} inversions in long array')
