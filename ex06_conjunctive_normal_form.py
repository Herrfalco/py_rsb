#!/usr/bin/python3

"Exercise 06 - Conjunctive normal form"

import copy
from formula import Formula
from ex02_gray_code import gray_code

def conjunctive_normal_form(form):
    'Return the conjunctive normal form of a formula'
    new_form = Formula(form)
    new_form.conv_2_cnf()
    return new_form.str

def test(): #pylint: disable=too-many-locals
    "Test function"
    tests = (('AB&!', 'A!B!|'),
             ('AB|!', 'B!A!&'),
             ('AB|C&', 'CBA|&'),
             ('AB|C|D|', 'BADC|||'),
             ('AB&C&D&', 'CDAB&&&'),
             ('AB&!C!|', 'B!A!C!||'),
             ('AB|!C!&', 'C!B!A!&&'),
             ('AB&CD&!|AB&|', 'AD!C!||BD!C!||&'),
             )
    print("{:40}".format("06 - Conjunctive normal form:"), end='')
    for form, exp in tests:
        result = conjunctive_normal_form(form)
        if result != exp:
            print(f"KO\n    \"conjunctive_normal_form(\'{form}\') = \'{result}\'\"")
            return
    for _ in range(200):
        form = Formula.random()
        old_form = copy.deepcopy(form)
        form.conv_2_cnf()
        if old_form.result != form.result:
            print(f"KO\n    \"conjunctive_normal_form(\'{old_form.str}\') = \'{form.str}\'\"")
            return
    v_lst = 'ABCDEF'
    for size in range(1, len(v_lst)):
        for _ in range(10):
            formu = Formula.random(rank=6, var_lst=v_lst[:size])
            var_lst = sorted(list({char for char in formu.str if char.isupper()}))
            for i in range(2 ** len(var_lst)):
                form_1 = formu.str
                form_2 = conjunctive_normal_form(form_1)
                pat = gray_code(i)
                new_form_1 = form_1
                new_form_2 = form_2
                for j, let in enumerate(var_lst):
                    new_form_1 = new_form_1.replace(let, str(pat >> j & 0x1))
                    new_form_2 = new_form_2.replace(let, str(pat >> j & 0x1))
                val_1 = Formula(new_form_1).result
                val_2 = Formula(new_form_2).result
                if val_1 != val_2:
                    print(f"KO\n    \"conjunctive_normal_form(\'{form_1}\') = \'{form_2}\'\"")
                    return
    print("OK")

if __name__ == '__main__':
    test()
