#!/usr/bin/python3

"Binary tree module that manipulates boolean expressions"

import sys
import copy
import random
from karnaugh import KTable

class FormIter: #pylint: disable=too-few-public-methods
    "Formula iterator"
    def __init__(self, form):
        self.gen = self._rec_iter(form.head)
    def __next__(self):
        return next(self.gen)
    def _rec_iter(self, node):
        for child in node['childs']:
            yield from self._rec_iter(child)
        yield node

class Formula:
    "Represent formula as binary tree"
    _node_types = {'!': {'childs': 1,
                         'value': lambda a: not a},
                   '&': {'childs': 2,
                         'value': lambda a, b: a & b,
                         'nnf': lambda a, b: {'type': '|', 'childs': [{
                             'type': '!', 'childs': [a]}, {'type': '!', 'childs': [b]}]}},
                   '|': {'childs': 2,
                         'value': lambda a, b: a | b,
                         'nnf': lambda a, b: {'type': '&', 'childs': [{
                             'type': '!', 'childs': [a]}, {'type': '!', 'childs': [b]}]},
                         'cnf': lambda a, b: {'type': '&', 'childs': [{
                             'type': '|', 'childs': [a['childs'][0], copy.deepcopy(b)]}, {
                                 'type': '|', 'childs': [a['childs'][1], b]}]}},
                   '^': {'childs': 2,
                         'value': lambda a, b: a ^ b,
                         'simp': lambda a, b: {'type': '&', 'childs': [{
                             'type': '|', 'childs': [copy.deepcopy(a), copy.deepcopy(b)]}, {
                                 'type': '!', 'childs': [{'type': '&', 'childs': [a, b]}]}]}},
                   '>': {'childs': 2,
                         'value': lambda a, b: (not a) | b,
                         'simp': lambda a, b: {'type': '|', 'childs': [{
                             'type': '!', 'childs': [a]}, b]}},
                   '=': {'childs': 2,
                         'value': lambda a, b: a == b,
                         'simp': lambda a, b: {'type': '|', 'childs': [{
                             'type': '&', 'childs': [copy.deepcopy(a), copy.deepcopy(b)]}, {
                                 'type': '!', 'childs': [{'type': '|', 'childs': [a, b]}]}]}}}

    @classmethod
    def _is_leaf(cls, char, sup=''):
        return char in ('01' + sup) or char.isupper()
    def _truth_table(self):
        letters = list({char for char in self.str if char.isupper()})
        letters.sort()
        vals = [sorted(letters) + ['=']]
        for pat in range(2 ** len(letters)):
            row = [str((pat >> shift) & 0b1) for shift in range(len(letters))]
            new_form = self.str
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
    @classmethod
    def _error(cls):
        "Display error and exit"
        print("Invalid formula", file=sys.stderr)
        sys.exit(1)
    @classmethod
    def _rand_util(cls, rank, var_lst):
        if not rank:
            return random.choice(var_lst if var_lst else '01')
        new_node = random.choices((var_lst if var_lst else '01') + '!&|^>=', (
            len(var_lst) if var_lst else 2) * [2] + [3, 3, 3, 3, 3, 3])[0]
        if new_node == '!':
            return cls._rand_util(rank - 1, var_lst) + new_node
        if new_node in '&|^>=':
            return cls._rand_util(rank - 1, var_lst) + \
                cls._rand_util(rank - 1, var_lst) + new_node
        return new_node
    @classmethod
    def random(cls, rank=3, var_lst=''):
        'Generate random formula'
        return Formula(cls._rand_util(rank, var_lst))

    def __init__(self, form):
        self.proc = None
        stack = []
        for char in form:
            if char in '01':
                if self.proc is False:
                    Formula._error()
                self.proc = True
            elif char.isupper():
                if self.proc:
                    Formula._error()
                self.proc = False
            elif char not in Formula._node_types.keys():
                Formula._error()
            try:
                childs = [stack.pop() for i in range(
                    Formula._node_types.get(char, {'childs': 0})['childs'])]
            except IndexError:
                Formula._error()
            stack.append({'type': char, 'childs': childs[::-1]})
        if len(stack) != 1:
            Formula._error()
        self.head = stack[0]
        self.height = 0
        self.repr = ''
        self.str = ''
        self.result = None
        self._update()
    def _copy(self, other):
        self.proc = other.proc
        self.head = other.head
        self.height = other.height
        self.repr = other.repr
        self.str = other.str
        self.result = other.result
    def __iter__(self):
        return FormIter(self)
    def __repr__(self):
        return self.repr
    def __str__(self):
        return self.str

    def _update(self):
        self.height = 0
        self.repr = ''
        self.str = ''
        self.result = None
        self._eval_height()
        self._eval_repr()
        self._eval_str()
        if self.proc:
            self._eval_result()
        else:
            self._eval_table()
    def _eval_height(self, node=None, height=None):
        if not node:
            node = self.head
            height = 1
        node['row'] = height - 1
        if height > self.height:
            self.height = height
        for child in node['childs']:
            self._eval_height(child, height + 1)
    def _get_sep(self, rnk):
        pad_sz = 2 ** abs(rnk - (self.height - 1)) - 1
        if not pad_sz:
            return ''
        return ' ' * (pad_sz // 2) + '.' + '-' * (pad_sz // 2)
    def _eval_repr(self):
        layout = [[] for _ in range(self.height)]
        for node in self:
            if node['type'] == '!':
                for i in range(1, self.height - node['row']):
                    layout[node['row'] + i].extend([' '] * (2 ** (i - 1)))
            elif Formula._is_leaf(node['type']):
                for i in range(1, self.height - node['row']):
                    layout[node['row'] + i].extend([' '] * (2 ** i))
            layout[node['row']].append(node['type'])
        tmp = []
        for (rnk, row) in enumerate(layout):
            sep = self._get_sep(rnk)
            line = ''
            for char in row:
                line += ((sep if not Formula._is_leaf(char, sup=' ') else ' ' * len(sep)) +
                         char + (sep[::-1] if not Formula._is_leaf(char, sup='! ') else ' ' *
                                 len(sep)) + ' ')
            tmp.append(line)
        self.repr = '\n'.join(tmp)
    def _eval_str(self):
        for node in self:
            self.str += node['type']
    def _truth_table(self):
        letters = list({char for char in self.str if char.isupper()})
        letters.sort()
        vals = [sorted(letters) + ['=']]
        for pat in range(2 ** len(letters)):
            row = [str((pat >> shift) & 0b1) for shift in range(len(letters))]
            new_form = self.str
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
    def _eval_result(self, node=None):
        if not node:
            node = self.head
        self.result = bool(int(node['type'])) if node['type'] in '01' else \
            Formula._node_types[node['type']]['value'](
                *[self._eval_result(child) for child in node['childs']])
        return self.result
    def _eval_table(self):
        self.result = self._truth_table()
    def _neg_simp(self):
        new_form = Formula(''.join((node['type'] for node in self)).replace('!!', ''))
        self._copy(new_form)
    def _sym_simp(self, node=None, parent=None):
        if not node:
            node = self.head
        for (idx, child) in enumerate(node['childs']):
            self._sym_simp(child, {'node': node, 'child': idx})
        if node['type'] in '^=>':
            new_node = Formula._node_types[node['type']]['simp'](*node['childs'])
            if parent:
                parent['node']['childs'][parent['child']] = new_node
            else:
                self.head = new_node
        self._update()
    def _nnf_util(self, node, pars):
        ret = False
        for i, child in enumerate(node['childs']):
            ret |= self._nnf_util(child, pars + [{'node': node, 'child': i}])
        if pars and pars[-1]['node']['type'] == '!' and not Formula._is_leaf(node['type']):
            new_node = Formula._node_types[node['type']]['nnf'](*node['childs'])
            if len(pars) > 1:
                pars[-2]['node']['childs'][pars[-2]['child']] = new_node
            else:
                self.head = new_node
            return True
        return ret
    def conv_2_nnf(self):
        "Put Formula into negative normal form"
        self._sym_simp()
        self._neg_simp()
        while self._nnf_util(self.head, []):
            self._neg_simp()
        self._update()
    def _cnf_util(self, node=None, parent=None):
        if not node:
            node = self.head
        ret = False
        for i, child in enumerate(node['childs']):
            ret |= self._cnf_util(child, {'node': node, 'child': i})
        new_node = None
        if node['type'] == '|':
            for i, child in enumerate(node['childs']):
                if child['type'] == '&':
                    new_node = Formula._node_types[node['type']]['cnf'](
                        *node['childs'][:: -1 if i else 1])
                    ret = True
                    break
        if new_node:
            if parent:
                parent['node']['childs'][parent['child']] = new_node
            else:
                self.head = new_node
        return ret
    def conv_2_cnf(self):
        "Put Formula into conjunctive normal form"
        if not {char for char in self.str if char.isupper()}:
            self.conv_2_nnf()
            while self._cnf_util():
                pass
            self._update()
        else:
            new_form = Formula(KTable.from_form(self.str).cnf())
            self._copy(new_form)

if __name__ == '__main__':
    pass
