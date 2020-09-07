import math


def split(x: int, m: int) -> (int, int):
    """
    split an integer into two parts where:
    x = x1 * 10 ** m + x0
    :param x: integer to be split
    :param m: number of digits to split
    :return: (x1, x0)
    """
    m = int(m)
    x1 = int(x // (10 ** m))
    x0 = int(x - x1 * (10 ** m))
    return x1, x0


def multiply(x: int, y: int) -> int:
    """
    multiply integers x and y using the karatsuba algorithm
    :param x:
    :param y:
    :return: product of x and y
    """
    if x < 10 and y < 10:
        return x * y
    else:
        m = (int(math.log10(max(x, y))) + 1) // 2
        x1, x0 = split(x, int(m))
        y1, y0 = split(y, int(m))
        z0 = multiply(x0, y0)
        z2 = multiply(x1, y1)
        z1 = multiply(x0 + x1, y0 + y1) - z0 - z2
        return int(z2 * (10 ** (2 * m)) + z1 * (10 ** m) + z0)


if __name__ == '__main__':
    import random

    x = random.getrandbits(64)
    y = random.getrandbits(64)
    print(f'x = {x}\ny = {y}')

    product = multiply(x, y)
    assert product == x * y
    print(f'x * y = {product}')
