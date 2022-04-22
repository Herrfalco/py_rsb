#!/usr/bin/python3

"Exercise 01 - Multiplier"

from ex00_adder import adder

def multiplier(lhs, rhs):
    "Multiply 2 numbers by using bitwise operators only"
    result = 0
    while rhs:
        if rhs & 0x1:
            result = adder(result, lhs)
        lhs = lhs << 1
        rhs = rhs >> 1
    return result

def test():
    "Test function"
    print("{:40}".format("01 - Multiplier:"), end='')
    for i in range(0, 0xff):
        for j in range(0, 0xff):
            result = multiplier(i, j)
            if result != i * j:
                print(f"KO\n    \"multiplier({i}, {j}) = {result}\"")
                return
    print("OK")

if __name__ == '__main__':
    test()
