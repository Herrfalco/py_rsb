#!/usr/bin/python3

"Exercise 02 - Gray code"

def gray_code(num):
    "Convert parameter into gray code"
    return num ^ (num >> 1)

def test():
    "Test Function"
    tests = ((0, 0), (1, 1), (2, 3),
             (3, 2), (4, 6), (5, 7),
             (6, 5), (7, 4), (8, 12))
    print("{:30}".format("02 - Gray code:"), end='')
    for num, exp in tests:
        result = gray_code(num)
        if result != exp:
            print("KO\n    \"gray_code({}) = {}\"".format(num, result))
            return
    print("OK")

if __name__ == '__main__':
    test()
