#!/usr/bin/python3

"Binary tree module that manipulates boolean expressions"

import sys
import copy

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
    """Represent formula as binary tree

       Attributes:

       *result* : formula's result
    """
    _node_types = {'0': {'childs': 0,
                         'value': lambda: False},
                   '1': {'childs': 0,
                         'value': lambda: True},
                   '!': {'childs': 1,
                         'value': lambda a: not a},
                   '&': {'childs': 2,
                         'value': lambda a, b: a & b,
                         'nnf': lambda a, b: {'type': '|', 'childs': [{
                             'type': '!', 'childs': [a]}, {'type': '!', 'childs': [b]}]}},
                   '|': {'childs': 2,
                         'value': lambda a, b: a | b,
                         'nnf': lambda a, b: {'type': '&', 'childs': [{
                             'type': '!', 'childs': [a]}, {'type': '!', 'childs': [b]}]}},
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
    def _error(cls):
        "Display error and exit"
        print("Invalid formula", file=sys.stderr)
        sys.exit(1)
    def __init__(self, form):
        stack = []
        for char in form:
            if char not in Formula._node_types.keys():
                Formula._error()
            try:
                childs = [stack.pop() for i in range(Formula._node_types[char]['childs'])]
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
        self._eval_result()
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
            elif node['type'] in ('0', '1'):
                for i in range(self.height - node['row']):
                    layout[node['row'] + i].extend([' '] * (i * 2))
            layout[node['row']].append(node['type'])
        tmp = []
        for (rnk, row) in enumerate(layout):
            sep = self._get_sep(rnk)
            line = ''
            for char in row:
                line += ((sep if char not in ('0', '1', ' ') else ' ' * len(sep)) + char +
                         (sep[::-1] if char not in ('0', '1', '!', ' ') else ' ' * len(sep)) + ' ')
            tmp.append(line)
        self.repr = '\n'.join(tmp)
    def _eval_str(self):
        for node in self:
            self.str += node['type']
    def _eval_result(self, node=None):
        if not node:
            node = self.head
        self.result = Formula._node_types[node['type']]['value'](
            *[self._eval_result(child) for child in node['childs']])
        return self.result
    def _neg_simp(self):
        new_form = Formula(''.join((node['type'] for node in self)).replace('!!', ''))
        self.head = new_form.head
        self.height = new_form.height
        self.repr = new_form.repr
        self.str = new_form.str
    def _sym_simp(self, node=None, parent=None):
        if not node:
            node = self.head
        for (idx, child) in enumerate(node['childs']):
            self._sym_simp(child, {'node': node, 'child': idx})
        if node['type'] in ('^', '=', '>'):
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
        if pars and pars[-1]['node']['type'] == '!' and node['type'] not in ('0', '1'):
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

if __name__ == '__main__':
    pass
