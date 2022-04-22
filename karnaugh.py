#!/usr/bin/python3

'Simplify boolean expression using Karnaugh table'

import copy
import sys
import formula
from ex02_gray_code import gray_code

class Coord: #pylint:disable=invalid-name
    'Two dimentional struct'
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __str__(self):
        return f'(x:{self.x},y:{self.y})'
    def __lt__(self, other):
        return self.area() < other.area()
    def area(self):
        'Return self area'
        return self.x * self.y
    def constrain(self, dim):
        'Return a copy of the object constained by dimensions in parameter'
        return Coord(self.x % dim.x, self.y % dim.y)
    def into(self, dim):
        'Return the index of self coordinates into dimensions in parameter'
        pos = self.constrain(dim)
        return pos.y * dim.x + pos.x
    def copy(self):
        'Return a copy of self'
        return Coord(self.x, self.y)

class ZoneIter: #pylint: disable=too-few-public-methods
    'Zone size iterator'
    def __init__(self, dim):
        self.max = dim
        self.gen = self._gen()
    def __next__(self):
        return next(self.gen)
    def __iter__(self):
        return self
    def _gen(self):
        area = self.max.area()
        coord = Coord()
        while area:
            coord.x = self.max.x
            while coord.x:
                coord.y = area // coord.x
                if 0 < coord.y <= self.max.y:
                    yield coord.copy()
                coord.x //= 2
            area //= 2

class KTable: #pylint: disable=invalid-name
    'Karnaugh table'
    @classmethod
    def _get_vars(cls, form):
        letters = sorted(list({char for char in form if char.isupper()}))
        x_vars = letters[:len(letters) // 2 + len(letters) % 2]
        y_vars = letters[len(x_vars):]
        return (x_vars, y_vars)
    @classmethod
    def from_form(cls, form):
        'Create a Karnaugh table from a formula'
        x_vars, y_vars = KTable._get_vars(form)
        dim = Coord(2 ** len(x_vars), 2 ** len(y_vars))
        true_v = []
        coord = Coord()
        for coord.y, pat_y in enumerate(map(gray_code, range(dim.y))):
            for coord.x, pat_x in enumerate(map(gray_code, range(dim.x))):
                new_form = form
                for pat, lets in [(pat_x, x_vars), (pat_y, y_vars)]:
                    for i, let in enumerate(lets[::-1]):
                        new_form = new_form.replace(let, str((pat >> i) & 0x1))
                if formula.Formula(new_form).result:
                    true_v.append(coord.into(dim))
        ktab = KTable(x_vars, y_vars, true_v)
        return ktab
    @classmethod
    def _error(cls):
        'Display error and exit'
        print('Invalid Karnaugh table', file=sys.stderr)
        sys.exit(2)
    def __init__(self, x_vars, y_vars, true_v=None):
        if not x_vars and not y_vars:
            KTable._error()
        for var in x_vars + y_vars:
            if len(var) != 1 or not var.isupper():
                KTable._error()
        self.x_vars = x_vars
        self.y_vars = y_vars
        self.dim = Coord(2 ** len(x_vars), 2 ** len(y_vars))
        self.table = [[False] * self.dim.x for i in range(self.dim.y)]
        self.zones = []
        if true_v:
            for v in true_v:
                if not 0 <= v < self.dim.x * self.dim.y:
                    KTable._error()
                self.table[v // self.dim.x][v % self.dim.x] = True
        self._find_all_zones()
        self._filter_zones()
    def __str__(self):
        return 'x: ' + str(self.x_vars) + '\n' + 'y: ' + str(self.y_vars) + '\n\n' + \
                '\n'.join(map(lambda row: ' '.join(
                    map(lambda cell: str(int(cell)), row)), self.table)) + '\n\n' + \
                        '\n'.join(map(str, self.zones))
    def _count(self):
        count = 0
        coord = Coord()
        for coord.y in range(self.dim.y):
            for coord.x in range(self.dim.x):
                if not self.table[coord.y][coord.x]:
                    count += 1
        return count
    def _test_zone(self, pos, dim):
        incl = set()
        coord = Coord()
        for coord.y in range(pos.y, pos.y + dim.y):
            for coord.x in range(pos.x, pos.x + dim.x):
                incl.add(coord.into(self.dim))
                mod = coord.constrain(self.dim)
                if self.table[mod.y][mod.x]:
                    return None
        return incl
    def _find_dim_zones(self, incl, dim):
        result = []
        coord = Coord()
        step = Coord(dim.x // 2, dim.y // 2)
        for coord.y in range(0, self.dim.y, step.y if step.y else 1):
            for coord.x in range(0, self.dim.x, step.x if step.x else 1):
                ret = self._test_zone(coord, dim)
                if ret and not ret.issubset(incl):
                    result.append(ret)
        return result
    def _find_all_zones(self):
        count = self._count()
        for dim in ZoneIter(self.dim):
            incl = {idx for zone in self.zones for idx in zone}
            if count == len(incl):
                return
            ret = self._find_dim_zones(incl, dim)
            self.zones.extend(ret)
        self.zones.sort(key=len)
    def _filter_zones(self):
        incl = {idx for zone in self.zones for idx in zone}
        idx = 0
        while idx < len(self.zones):
            new_zones = copy.copy(self.zones)
            new_zones.pop(idx)
            if {idx for zone in new_zones for idx in zone} == incl:
                self.zones = new_zones
            else:
                idx += 1
    @classmethod
    def _gray_2_var(cls, ones, zeros, var_lst):
        result = []
        for shift, var in enumerate(var_lst[::-1]):
            if ones & (0x1 << shift):
                result.append(var + '!')
            elif zeros & (0x1 << shift):
                result.append(var)
        return result
    def cnf(self):
        'Return CNF from Karnaugh Table'
        result = ''
        if not self.zones:
            return '1'
        for zone in self.zones:
            if len(zone) == self.dim.area():
                return '0'
            x_true, x_false = 2 ** len(self.x_vars) - 1, 0
            y_true, y_false = 2 ** len(self.y_vars) - 1, 0
            for idx in zone:
                x, y = idx % self.dim.x, idx // self.dim.x
                x_true &= gray_code(x)
                y_true &= gray_code(y)
                x_false |= gray_code(x)
                y_false |= gray_code(y)
            dis_res = KTable._gray_2_var(x_true, ~x_false & 2
                                         ** len(self.x_vars) - 1, self.x_vars)
            dis_res.extend(KTable._gray_2_var(y_true, ~y_false & 2
                                              ** len(self.y_vars) - 1, self.y_vars))
            result += ''.join(dis_res) + '|' * (len(dis_res) - 1)
        result += '&' * (len(self.zones) - 1)
        return result

if __name__ == '__main__':
    pass
