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
    print("{:40}".format("\00100 - Adder:"), end='')
    for i in range(0, 0xff):
        for j in range(0, 0xff):
            result = adder(i, j)
            if result != i + j:
                print(f"KO\n    \"adder({i}, {j}) = {result}\"")
                return
    print("OK")

if __name__ == '__main__':
    test()
