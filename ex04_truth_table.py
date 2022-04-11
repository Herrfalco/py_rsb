#!/usr/bin/python3

"Exercise 04 - Truth table"

from formula import Formula

def truth_table(form):
    "Compute truth table of a boolean expression"
    letters = list({char for char in form if char.isupper()})
    letters.sort()
    vals = [sorted(letters) + ['=']]
    for pat in range(2 ** len(letters)):
        row = [str((pat >> shift) & 0b1) for shift in range(len(letters))]
        new_form = form
        for (i, let) in enumerate(letters):
            new_form = new_form.replace(let, row[i])
        row.append(str(int(Formula(new_form).result)))
        vals.append(row)
    result = []
    for (i, row) in enumerate(vals):
        result.append('| ' + ' | '.join(row) + ' |')
        if not i:
            result.append('|---' * len(row) + '|')
    return '\n'.join(result)

def print_truth_table(form):
    "Print the truth table of a boolean expression"
    print(truth_table(form))

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
        result = truth_table(form)
        if result != exp:
            print("KO\n    \"eval_formula({}) = \n{}\"".format(form, result))
            return
    print("OK")

if __name__ == '__main__':
    test()
