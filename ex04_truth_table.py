#!/usr/bin/python3

"Exercise 04 - Truth table"

from formula import Formula

def print_truth_table(form):
    "Print the truth table of a boolean expression"
    print(Formula(form).result)

def test():
    "Test function"
    tests = (('AA&', """| A | = |
|---|---|
| 0 | 0 |
| 1 | 1 |"""),
             ('AB|', """| A | B | = |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 1 |"""),
             ('ABB=|', """| A | B | = |
|---|---|---|
| 0 | 0 | 1 |
| 1 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 1 |"""),
             ('BA=CDA^|>', """| A | B | C | D | = |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 |
| 0 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 | 1 |
| 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 1 | 0 |
| 0 | 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 | 1 |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 1 |"""),
             ('AA|BB^&', """| A | B | = |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 1 | 0 |"""),
             ('C', """| C | = |
|---|---|
| 0 | 0 |
| 1 | 1 |"""),
             ('AA=AA==', """| A | = |
|---|---|
| 0 | 1 |
| 1 | 1 |"""))

    print("{:30}".format("04 - Truth table:"), end='')
    for form, exp in tests:
        result = Formula(form).result
        if result != exp:
            print("KO\n    \"eval_formula(\'{}\') = \'{}\'\"".format(form, result))
            return
    print("OK")

if __name__ == '__main__':
    test()
