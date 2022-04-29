#!/usr/bin/python3

'Exercise 11 - Inverse function'

import itertools as it
from ex10_curve import my_map

#pylint: disable=redefined-builtin, invalid-name

def reverse_map(value):
    'Return coordinates for each value'
    if not 0 <= value <= 1:
        return None
    value = int(value * (2 ** 32)) if value else 0
    x, y = 0, 0
    for i in range(16)[::-1]:
        x <<= 1
        y <<= 1
        x |= int(bool(value & (0x1 << (i * 2))))
        y |= int(bool(value & (0x1 << (i * 2 + 1))))
    return x, y

def test():
    'Test function'
    print("{:40}".format("\00111 - Inverse function:"), end='')
    tests = ({'value': -1, 'result': None},
             {'value': 1.1, 'result': None})

    for y in it.chain(range(0, 256), range(2 ** 16 - 256, 2 ** 16)):
        for x in it.chain(range(0, 256), range(2 ** 16 - 256, 2 ** 16)):
            result = reverse_map(my_map(x, y))
            if (x, y) != reverse_map(my_map(x, y)):
                print(f"KO\n    \"reverse_map(my_map({x}, {y})) = {result}\"")
                return
    for tst in tests:
        result = reverse_map(tst['value'])
        if result != tst['result']:
            print(f"KO\n    \"reverse_map({tst['value']}) = {result}\"")
            return
    print('OK')

if __name__ == '__main__':
    test()
