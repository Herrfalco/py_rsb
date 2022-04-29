#!/usr/bin/python3

'Exercise 09 - Set evaluation'

SET_OP = {'!': {'att_nb': 1, 'fn': lambda enc, a: enc - a},
           '&': {'att_nb': 2, 'fn': lambda enc, a, b: a & b},
           '|': {'att_nb': 2, 'fn': lambda enc, a, b: a | b},
           '^': {'att_nb': 2, 'fn': lambda enc, a, b: (a | b) - (a & b)},
           '>': {'att_nb': 2, 'fn': lambda enc, a, b: (enc - a) | b},
           '=': {'att_nb': 2, 'fn': lambda enc, a, b: (a & b) | ((enc - a) & (enc - b))}}

def eval_set(form, sets):
    'Evaluate set formula'
    set_names = sorted(list({char for char in form if char.isupper()}))
    if len(sets) != len(set_names):
        return None
    enc = set()
    for elem in sets:
        enc.update(set(elem))
    stack = []
    for char in form:
        if char.isupper():
            stack.append(set(sets[set_names.index(char)]))
        else:
            try:
               set_op = SET_OP[char]
               params, stack = stack[set_op['att_nb'] * -1:], stack[:set_op['att_nb'] * -1]
               stack.append(set_op['fn'](enc, *params))
            except (KeyError, TypeError):
                return None
    if len(stack) != 1:
        return None
    return sorted(list(stack[0]))


def test():
    'Test function'
    print("{:40}".format("\00109 - Set evaluation:"), end='')
    test_lst = ({'form': 'AB&C|!', 'sets': [[1, 2, 3], [7, 3, 4], [4, 5, 6]], 'result': [1, 2, 7]},
                {'form': 'AB&', 'sets': [[0, 1, 2], [0, 3, 4]], 'result': [0]},
                {'form': 'AB|', 'sets': [[0, 1, 2], [3, 4, 5]], 'result': [0, 1, 2, 3, 4, 5]},
                {'form': 'A!', 'sets': [[0, 1, 2]], 'result': []},
                {'form': 'AB?', 'sets': [[1, 2], [4, 5]], 'result': None},
                {'form': '^', 'sets': [], 'result': None},
                {'form': 'AA^', 'sets': [[1, 2]], 'result': []})
    for test in test_lst:
        result = eval_set(test['form'], test['sets'])
        if result != test['result']:
            print(f"KO\n    \"eval_set(\'{test['form']}\', {test['sets']}) = {result}\"")
            return
    print('OK')

if __name__ == '__main__':
    test()
