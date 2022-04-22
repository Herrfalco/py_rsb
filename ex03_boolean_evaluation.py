#!/usr/bin/python3

"Exercise 03 - Boolean evaluation"

from formula import Formula

def eval_formula(form):
    "Evaluate boolean expression"
    return Formula(form).result

def test():
    "Test function"
    tests = (('0', False), ('1', True),
             ('00&', False), ('01&', False), ('10&', False), ('11&', True),
             ('00|', False), ('01|', True), ('10|', True), ('11|', True),
             ('00^', False), ('01^', True), ('10^', True), ('11^', False),
             ('00>', True), ('01>', True), ('10>', False), ('11>', True),
             ('00=', True), ('01=', False), ('10=', False), ('11=', True),
             ('1011||=', True), ('10&1!^11=|0!1>^', False), ('011^00==>101=>&', False),
             ('101=>00=11^=0>&', False))
    print("{:40}".format("03 - Boolean evaluation:"), end='')
    for form, exp in tests:
        result = eval_formula(form)
        if result != exp:
            print(f"KO\n    \"eval_formula(\'{form}\') = {result}\"")
            return
    print("OK")

if __name__ == '__main__':
    test()
