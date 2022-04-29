#!/usr/bin/python3

'Execute all rsb tests'

import os
import sys

class ResultList:
    def __init__(self):
        self.data = []
    def write(self, data):
        self.data.append(data)

TMP_FILE = '.tmp'

def _test():
    childs = 0
    pid = None
    try:
        os.remove(TMP_FILE)
    except FileNotFoundError:
        pass
    with open(TMP_FILE, 'a') as out_put:
        for file in sorted(os.listdir(os.getcwd())):
            if file[:2] == 'ex':
                pid = os.fork()
                if not pid:
                    os.dup2(out_put.fileno(), 1)
                    os.execv('./' + file, [file])
                childs += 1
        for _ in range(childs):
            os.waitpid(-1, 0)
            os.system('clear')
            with open(TMP_FILE, 'r') as in_put:
                for line in sorted(in_put.read().split(sep='\001')):
                    print(line, end='')
    os.remove(TMP_FILE)

if __name__ == '__main__':
    _test()
