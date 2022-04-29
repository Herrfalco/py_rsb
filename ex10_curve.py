#!/usr/bin/python3

'Exercise 10 - Curve'

import itertools as it

#pylint: disable=redefined-builtin, invalid-name

class IntIter:
    'Integer binary iterator'
    def __init__(self, val, size):
        self.val = val
        self.shift = size
    def __iter__(self):
        return self
    def __next__(self):
        if self.shift < 1:
            raise StopIteration
        self.shift -= 1
        return (self.val >> self.shift) & 0x1


def my_map(x, y):
    'Return a unique value for each combination of coordinates'
    if not x in range(2 ** 16) or not y in range(2 ** 16):
        return None
    result = 0
    for val in map(lambda pack: (pack[0] << 1) | pack[1], zip(IntIter(y, 16), IntIter(x, 16))):
        result <<= 2
        result |= val
    return result / 2 ** 32

def test():
    'Test function'
    print("{:40}".format("\00110 - Curve:"), end='')
    tests = ({'x': 2 ** 16, 'y': 0, 'result': None},
             {'x': -1, 'y': 0, 'result': None})
    total_vals = []
    for y in it.chain(range(256), range(2 ** 16 - 256, 2 ** 16)):
        for x in it.chain(range(256), range(2 ** 16 - 256, 2 ** 16)):
            result = my_map(x, y)
            if not 0 <= result <= 1:
                print(f"KO\n    \"my_map({x}, {y}) = {result}\"")
            total_vals.append(my_map(x, y))
    if len(total_vals) != len(set(total_vals)):
        print(f"KO\n    \"my_map is not a bijective function\"")
        return
    for tst in tests:
        result = my_map(tst['x'], tst['y'])
        if result != tst['result']:
            print(f"KO\n    \"my_map({tst['x']}, {tst['y']}) = {result}\"")
            return
    print('OK')

if __name__ == '__main__':
    test()
