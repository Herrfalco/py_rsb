#!/usr/bin/python3

"Exercise 07 - SAT"

from formula import Formula

def sat(form):
    "Return True if formula is satisfiable else False"
    return Formula(form).sat

def test():
    "Test function"
    tests = (('AB|', True),
             ('AB&', True),
             ('AB&CD|^', True),
             ('AA!&', False),
             ('AA^', False),
             ('AB&AB&!&', False))

    print("{:40}".format("\00107 - SAT:"), end='')
    for form, exp in tests:
        result = Formula(form).sat
        if result != exp:
            print(f"KO\n    \"sat(\'{form}\') = \'{result}\'\"")
            return
    print("OK")

if __name__ == '__main__':
    test()
