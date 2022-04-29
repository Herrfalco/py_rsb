#!/usr/bin/python3

'Exercise 08 - Powerset'

from math import factorial

def _rec_pset(in_set, base_set=None):
    if not base_set:
        base_set = set()
    result = set()
    for elem in in_set:
        result |= _rec_pset(in_set - {elem}, base_set | {elem})
    result.add(frozenset(base_set))
    return result

def powerset(in_set):
    'Return power set of a set'
    result = _rec_pset(set(in_set))
    return sorted([list(elem) for elem in result])

def _comb_nb(objs, samp):
    return factorial(objs) // (factorial(samp) * factorial(objs - samp))

def test():
    'Test function'
    print("{:40}".format("\00108 - Powerset:"), end='')
    test_lst = []
    for i in range(10):
        pset = powerset(test_lst)
        if len(pset) != 2 ** len(test_lst):
            print(f"KO\n    \"powerset(\'{test_lst}\') = \'{pset}\'\"")
        for j in range(len(test_lst) + 1):
            sel = [frozenset(elem) for elem in pset if len(elem) == j]
            if len(sel) != _comb_nb(len(test_lst), j) or len(set(sel)) != len(sel):
                print(f"KO\n    \"powerset(\'{test_lst}\') = \'{pset}\'\"")
        test_lst.append(i)
    print('OK')

if __name__ == '__main__':
    test()
