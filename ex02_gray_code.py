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
    print("{:40}".format("\00102 - Gray code:"), end='')
    for num, exp in tests:
        result = gray_code(num)
        if result != exp:
            print(f"KO\n    \"gray_code({num}) = {result}\"")
            return
    print("OK")

if __name__ == '__main__':
    test()
