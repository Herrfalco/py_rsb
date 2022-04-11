#!/usr/bin/python3

"""
Execute all rsb tests
"""

import os

def test():
    """
    Test function
    """
    for file in sorted(os.listdir(os.getcwd())):
        if file[:2] == 'ex':
            pid = os.fork()
            if pid:
                os.waitpid(pid, 0)
            else:
                os.execv('./' + file, [file])

if __name__ == '__main__':
    test()
