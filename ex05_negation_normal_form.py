#!/usr/bin/python3

"Exercise 05 - Negation normal form"

import copy
from formula import Formula

def negation_normal_form(form):
    'Return the negation normal form of a formula'
    new_form = Formula(form)
    new_form.conv_2_nnf()
    return new_form.str

def test():
    "Test function"
    tests = (('AB&!', 'A!B!|'),
             ('AB|!', 'A!B!&'),
             ('AB>', 'A!B|'),
             ('AB=', 'AB&A!B!&|'),
             ('AB|C&!', 'A!B!&C!|'),
             )

    print("{:40}".format("\00105 - Negation normal form:"), end='')
    for form, exp in tests:
        result = negation_normal_form(form)
        if result != exp:
            print(f"KO\n    \"negation_normal_form(\'{form}\') = \'{result}\'\"")
            return
    for _ in range(200):
        form = Formula.random()
        old_form = copy.deepcopy(form)
        form.conv_2_nnf()
        if old_form.result != form.result:
            print(f"KO\n    \"negation_normal_form(\'{old_form.str}\') = \'{form.str}\'\"")
            return
    for _ in range(200):
        form = Formula.random(var_lst='ABC')
        old_form = copy.deepcopy(form)
        form.conv_2_nnf()
        if old_form.result != form.result:
            print(f"KO\n    \"negation_normal_form(\'{old_form.str}\') = \'{form.str}\'\"")
            return
    print("OK")

if __name__ == '__main__':
    test()
