#!/usr/bin/python3

"Exercise 00 - Adder"

def adder(lhs, rhs):
    "Add 2 numbers by using bitwise operators only"
    while rhs:
        carry = lhs & rhs
        lhs = lhs ^ rhs
        rhs = carry << 1
    return lhs

def test():
    "Test function"
    print("{:30}".format("00 - Adder:"), end='')
    for i in range(0, 0xff):
        for j in range(0, 0xff):
            result = adder(i, j)
            if result != i + j:
                print("KO\n    \"adder({}, {}) = {}\"".format(i, j, result))
                return
    print("OK")

if __name__ == '__main__':
    test()
